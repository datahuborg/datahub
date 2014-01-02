package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

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
import Annotations.column.AssociationType;
import Annotations.database;
import Annotations.column.Index;
import DataHubAccount.DataHubAccount;
import DataHubResources.Resources;

@database(name="")
public abstract class Database {
	
	protected static int MAX_LOAD_RECURSION_DEPTH = 3;
	
	//prevent do unnecessary saves
	protected static int MAX_SAVE_RECURSION_DEPTH = 2;
	
	private DataHubClient dhc;
	
	private ConcurrentHashMap<String,Object> cache;
	
	public Database(){
		this.cache = new ConcurrentHashMap<String,Object>();
	}
	protected void resetCacheEntry(String key){
		if(cache.containsKey(key)){
			cache.remove(key);
		}
	}
	protected void resetCache(){
		cache = new ConcurrentHashMap<String,Object>();
	}
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
	private DHQueryResult dbQuery(String query){
		//System.out.println(query);
		//System.out.println(dhc.dbQuery(query));
		return dhc.dbQuery(query);
	}
	protected void query(String query){
		dhc.dbQuery(query);
	}
	protected <T extends Model> ArrayList<T> query(String query, Class<T> modelClass, int recursionDepthLimit){
		ArrayList<T> output = new ArrayList<T>();
		if(recursionDepthLimit <= 0){
			return output;
		}
		//non-static implementation (should be static though)
		//get table name
		//get model class name
		//make query to datahub and create new instances 
		try{
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			//System.out.println(this.dbQuery(query));
			if(query.toLowerCase().contains("select") && cache.containsKey(query)){
				output = (ArrayList<T>) cache.get(query);
				//System.out.println("RECURSION DEPTH: "+recursionDepthLimit);
				//System.out.println("cache hit "+query);
				//System.out.println(output);
			}else{
				output = dhQueryToModel(this.dbQuery(query), modelClass,recursionDepthLimit-1);
				cache.put(query, output);
				//System.out.println("cache miss "+query );
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	protected <T extends Model> void updateModelObject(T model){
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateSQLRep("AND");
		//System.out.println(query);
		DHQueryResult dhqr = this.dbQuery(query);
		updateNewModel(dhqr, 0, model, Database.MAX_LOAD_RECURSION_DEPTH);
	}
	protected <T extends Model> void updateModelId(T model){
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateSQLRep("AND");
		DHQueryResult dhqr = this.dbQuery(query);
		updateNewModel(dhqr, 0, model, Database.MAX_LOAD_RECURSION_DEPTH, true);
	}
	public <T extends Model> ArrayList<T> query(String query, Class<T> modelClass){
		return query(query,modelClass,Database.MAX_LOAD_RECURSION_DEPTH);
	}
	private <T extends Model> ArrayList<T> dhQueryToModel(DHQueryResult dhqr, Class<T> modelClass, int recursionDepthLimit) throws InstantiationException, IllegalAccessException{
		ArrayList<T> output = new ArrayList<T>();
		if(dhqr == null){
			return output;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = (T) modelClass.newInstance();
			updateNewModel(dhqr, i,newObj,recursionDepthLimit);
			output.add(newObj);
		}
		return output;
	}
	private <T extends Model> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate, int recursionDepthLimit){
		updateNewModel(dhqr, rowNumber, objectToUpdate, recursionDepthLimit, false);
	}
	private <T extends Model> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate, int recursionDepthLimit, boolean idOnly){
		String databaseName = this.getDatabaseName();
		String tableName = objectToUpdate.getTableName();
		String completeTableName = objectToUpdate.getCompleteTableName();
		
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		HashMap<String,DHCell> fieldsToDHCell = new HashMap<String,DHCell>();
		
		//invalid conditions, terminate
		if(table.rows.size() == 0){
			return;
		}
		
		//TODO: ID issues
		DHRow row = table.rows.get(rowNumber);
		List<DHField> fields = schema.getFields();
		for(int j = 0; j < fields.size(); j++){
			DHField f = fields.get(j);
			DHCell v = row.getCells().get(j);
			fieldsToDHCell.put(f.name, v);
		}
		//TODO: ID issues
		//ensure id is set before anything and only set the id if the object has an invalid id
		if(!objectToUpdate.validId()){
			if(fieldsToDHCell.containsKey("id")){
				DHCell cell_id = fieldsToDHCell.get("id");
				Resources.setField(objectToUpdate, "id", cell_id.value);
			}else{
				//TODO: throw exception here
			}
		}
		if(!idOnly){
			for(Field f1:objectToUpdate.getClass().getFields()){
				//skip setting the id because it was set above
				if(f1.getName().equals("id")){
					continue;
				}
				if(f1.isAnnotationPresent(column.class)){
					column c = f1.getAnnotation(column.class);
					if(c.RelationType() == AssociationType.None){
						if(fieldsToDHCell.containsKey(c.name())){
							DHCell cell = fieldsToDHCell.get(c.name());
							Resources.setField(objectToUpdate, c.name(), cell.value);
						}
					}
					//TODO:Fix this
					if(c.RelationType() == AssociationType.HasOne){
						if(DataHubConverter.isModelSubclass(f1.getType())){
							try{
								DHCell cell = fieldsToDHCell.get(c.name());
								Model m = (Model) f1.getType().newInstance();
								String newCompleteTableName = m.getCompleteTableName();
								String query = "select * from "+newCompleteTableName+" where "+newCompleteTableName+"."+c.name()+"="+objectToUpdate.id+" LIMIT 1";
								ArrayList<T> newData = (ArrayList<T>) this.query(query, m.getClass(),recursionDepthLimit);
								if(newData.size() > 0){
									Resources.setField(objectToUpdate, f1.getName(),newData.get(0));
								}
							}catch(Exception e){
								e.printStackTrace();
							}
						}
					}
					if(c.RelationType() == AssociationType.BelongsTo){
						if(DataHubConverter.isModelSubclass(f1.getType())){
							try{
								DHCell cell = fieldsToDHCell.get(c.name());
								int modelObjectBelongsToId = (int) Resources.convert(cell.value, Integer.TYPE);
								//TODO: object already in memory so can just re-use it instead of making new query
								Model m = (Model) f1.getType().newInstance();
								String newCompleteTableName = m.getCompleteTableName();
								//String query = "select * from "+completeTableName+", "+newCompleteTableName+" where "+tableName+".id = "+objectToUpdate.id;
								String query = "select * from "+newCompleteTableName+" where "+newCompleteTableName+".id = "+modelObjectBelongsToId+" LIMIT 1";
								//System.out.println(query);
								ArrayList<T> newData = (ArrayList<T>) this.query(query, m.getClass(),recursionDepthLimit);
								if(newData.size() > 0){
									Resources.setField(objectToUpdate, f1.getName(),newData.get(0));
								}
							}catch(Exception e){
								
							}
						}
					}
					if(c.RelationType() == AssociationType.HasMany){
						Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) f1.getType();
						if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
							//fix this
							//make sure id of this object is set before doing this
							try{
								DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
								d.setCurrentModel(objectToUpdate);
								d.setDatabase(this);
								d.setForeignKey(c.name());
								d.populate(recursionDepthLimit);
								Resources.setField(objectToUpdate, f1.getName(),d);
							}catch(Exception e){
								e.printStackTrace();
							}
						}
					}
					//TODO:fix this
					if(c.RelationType() == AssociationType.HasAndBelongsToMany){
						
					}
				}
			}
		}
	}
}
