package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import org.apache.thrift.TException;

import datahub.DHCell;
import datahub.DHData;
import datahub.DHException;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;

import Annotations.column;
import Annotations.database;
import Annotations.column.Index;
import DataHubAccount.DataHubAccount;
import DataHubResources.Resources;

@database(name="")
public abstract class Database {

	private DataHubClient dhc;
	
	public void setDataHubAccount(DataHubAccount dha){
		this.dhc = new DataHubClient(dha);
	}
	public void connect() throws DataHubException{
		try {
			dhc.connect(this);
		} catch (Exception e){
			//fix this
			throw new DataHubException("Cannot connect to database!");
		}
		instantiateAndSetup();
	}
	public void disconnect(){
		dhc.disconnect();
	}
	private void instantiateAndSetup(){
		ArrayList<Field> fields = DataHubConverter.findModels(this);
		for(Field f:fields){
			Resources.setField(this,f.getName(), Resources.fieldToInstance(f));
			try{
				//TODO: somehow make this static
				((Model) f.get(this)).setDatabase(this);
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	}
	public String getDatabaseName(){
		database d = this.getClass().getAnnotation(database.class);
		if(d != null){
			return d.name();
		}
		return null;
	}
	protected DHQueryResult dbQuery(String query){
		return dhc.dbQuery(query);
	}
	protected <Q> String converToSQLAndConcatenate(Iterable<Q> i, String linkSymbol){
		ArrayList<String> sqlVersions = new ArrayList<String>();
		for(Q object: i){
			String objStr = Resources.objectToSQL(object);
			sqlVersions.add(objStr);
		}
		return Resources.concatenate(sqlVersions,linkSymbol);
	}
	protected <T extends Model> ArrayList<T> query(String query, T currentModel){
		ArrayList<T> output = new ArrayList<T>();
		//non-static implementation (should be static though)
		//get table name
		//get model class name
		//make query to datahub and create new instances 
		try{
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			//System.out.println(query);
			//System.out.println(this.dbQuery(query));
			output = dhQueryToModel(this.dbQuery(query), currentModel);
			
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	protected <T extends Model> ArrayList<T> dhQueryToModel(DHQueryResult dhqr, T currentModel) throws InstantiationException, IllegalAccessException{
		ArrayList<T> output = new ArrayList<T>();
		if(dhqr == null){
			return output;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = (T) currentModel.getClass().newInstance();
			updateNewModel(dhqr, i,newObj);
			output.add(newObj);
		}
		return output;
	}
	protected <T extends Model> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate){
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		HashMap<String,DHCell> fieldsToDHCell = new HashMap<String,DHCell>();
		//TODO: ID issues
		if(table.rows.size() > 0){
			DHRow row = table.rows.get(rowNumber);
			List<DHField> fields = schema.getFields();
			for(int j = 0; j < fields.size(); j++){
				DHField f = fields.get(j);
				DHCell v = row.getCells().get(j);
				fieldsToDHCell.put(f.name, v);
			}
		}
		
		//ensure id is set before anything
		DHCell cell_id = fieldsToDHCell.get("id");
		Resources.setField(objectToUpdate, "id", cell_id.value);
		
		for(Field f1:objectToUpdate.getClass().getFields()){
			if(f1.isAnnotationPresent(column.class)){
				column c = f1.getAnnotation(column.class);
				if(c.Index() == Index.None){
					if(fieldsToDHCell.containsKey(c.name())){
						DHCell cell = fieldsToDHCell.get(c.name());
						Resources.setField(objectToUpdate, c.name(), cell.value);
					}
				}
				if(c.Index() == Index.LinkedSet){
					DHCell cell = fieldsToDHCell.get(c.name());
					Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) f1.getType();
					if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
						//fix this
						//make sure id of this object is set before doing this
						try{
							DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
							d.setCurrentModel(objectToUpdate);
							d.setDatabase(this);
							d.populate();
							Resources.setField(objectToUpdate, f1.getName(),d);
						}catch(Exception e){
							e.printStackTrace();
						}
					}
				}
			}
		}
	}
}
