package DataHubORM;

import java.util.ArrayList;
import java.util.List;

import datahub.DHCell;
import datahub.DHData;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;

import Annotations.column;
import Annotations.database;
import Annotations.table;
import DataHubORMTests.TestModel;
import DataHubResources.Resources;

@table(name="")
public class Model<T>{
	
	private Database db;
	
	@column
	public int id;

	public Model(){
		
	}
	public void setDatabase(Database db){
		this.db = db;
	}
	public void save(){
	}
	public void update(){
	}
	public void destroy(){
	}
	public ArrayList<T> findAll(){
		
		//non-static implementation (should be static though)
		//get table name
		//get model class name
		//make query to datahub and create new instances 
		ArrayList<T> output = new ArrayList<T>();
		try{
			output = dhQueryToModel(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	private ArrayList<T> dhQueryToModel(DHQueryResult dhqr) throws InstantiationException, IllegalAccessException{
		ArrayList<T> output = new ArrayList<T>();
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = newInstance();
			DHRow row = table.rows.get(i);
			List<DHField> fields = schema.getFields();
			for(int j = 0; j < fields.size(); j++){
				DHField f = fields.get(j);
				DHCell v = row.getCells().get(j);
				//maybe move this somewhere
				Resources.setField(newObj, f.name, v.value);
			}
			output.add(newObj);
		}
		return output;
	}
	public T test() throws NoSuchFieldException, SecurityException, IllegalArgumentException, IllegalAccessException, InstantiationException{
		T obj = newInstance();
		Resources.setField(obj, "name", "david");
		return obj;
	}
	private T newInstance() throws InstantiationException, IllegalAccessException{
		return (T) getClass().newInstance();
	}
	public String getTableName(){
		table t = this.getClass().getAnnotation(table.class);
		if(t != null){
			return t.name();
		}
		return null;
	}
}
