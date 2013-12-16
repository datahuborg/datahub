package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import datahub.DHCell;
import datahub.DHData;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;
import datahub.DHType;

import Annotations.column;
import Annotations.database;
import Annotations.table;
import DataHubORMTests.TestModel;
import DataHubResources.Resources;

@table(name="")
public class Model<T extends Model>{
	
	private static Database db;
	
	@column(name="id")
	public int id;

	public Model(){
		this.id = 0;
	}
	public static void setDatabase(Database db){
		Model.db = db;
	}
	public static Database getDatabase(){
		return db;
	}
	public void save(){
		try{
			String query = "";
			//fix this
			if(this.id <= 0){
				query = "INSERT INTO "+this.getCompleteTableName()+"("+this.getFieldNames()+")"+" VALUES( "+getFieldValues()+")";
				System.out.println(query);
			}else{
				query = "UPDATE "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.id;
			}
			DHQueryResult dhqr = db.dbQuery(query);
			updateModel();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public void destroy(){
		try{
			String query = "DELETE FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.id;
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			System.out.println(query);
			db.dbQuery(query);
			//possibly garbage collect object
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public ArrayList<T> all(){
		String query = "select * FROM "+this.getCompleteTableName();
		return query(query);
	}
	public ArrayList<T> findAll(HashMap<String,Object> params){
		String query = "select * FROM "+this.getCompleteTableName()+" WHERE "+ queryToSQL(params);
		return query(query);
	}
	public T findOne(HashMap<String,Object> params){
		String query = "select * FROM "+this.getCompleteTableName()+" WHERE "+ queryToSQL(params) +" LIMIT 1";
		if(query(query).size() > 0){
			return query(query).get(0);
		}
		return null; 
	}
	private ArrayList<T> query(String query){
		ArrayList<T> output = new ArrayList<T>();
		//non-static implementation (should be static though)
		//get table name
		//get model class name
		//make query to datahub and create new instances 
		try{
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			output = dhQueryToModel(db.dbQuery(query));
			
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	private String queryToSQL(HashMap<String,Object> query){
		String out = "";
		int counter = 0;
		int size = query.keySet().size();
		for(String field:query.keySet()){
			counter++;
			if(Resources.hasField(this.getClass(), field)){
				String val = Resources.objectToSQL(query.get(field));
				out+=field+"="+val;
				if(counter < size){
					out+=",";
				}
			}			
		}
		return out;
	}
	private String generateSQLRep(){
		String out ="";
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		int counter = 0;
		int size = currentModel.keySet().size();
		for(String field:currentModel.keySet()){
			counter++;
			if(field!="id"){
				String val = Resources.getFieldStringRep(this,field);
				out+=field+"="+val;
				if(counter < size){
					out+=",";
				}
			}
		}
		return out;
	}
	private String getFieldNames(){
		String out ="";
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		int counter = 0;
		int size = currentModel.keySet().size();
		for(String field:currentModel.keySet()){
			counter++;
			out+=field;
			if(counter < size){
				out+=",";
			}
		}
		return out;
	}
	private String getFieldValues(){
		String out ="";
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		int counter = 0;
		int size = currentModel.keySet().size();
		for(String field:currentModel.keySet()){
			counter++;
			out+=Resources.getFieldStringRep(this,field);;
			if(counter < size){
				out+=",";
			}
		}
		return out;
	}
	private ArrayList<T> dhQueryToModel(DHQueryResult dhqr) throws InstantiationException, IllegalAccessException{
		ArrayList<T> output = new ArrayList<T>();
		if(dhqr == null){
			return output;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = newInstance();
			updateNewModel(dhqr, i,newObj);
			output.add(newObj);
		}
		return output;
	}
	private void updateModel(){
		//worry about casting issues here
		String query = "SELECT * FROM "+ this.getCompleteTableName()+" WHERE  id="+this.id;
		DHQueryResult dhqr = this.db.dbQuery(query);
		updateNewModel(dhqr,0,(T)this);
	}
	private void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate){
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		if(table.rows.size() > 0){
			DHRow row = table.rows.get(rowNumber);
			List<DHField> fields = schema.getFields();
			for(int j = 0; j < fields.size(); j++){
				DHField f = fields.get(j);
				DHCell v = row.getCells().get(j);
				try{
					Field f1 = this.getClass().getField(f.name);
					if(f.name.equals("id")){
						objectToUpdate.id = (int)Resources.convert(v.value, Integer.TYPE);
					}
					if(f1.isAnnotationPresent(column.class)){
						Resources.setField(objectToUpdate, f.name, v.value);
					}
				}catch(Exception e){
					
				}
			}
		}
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
	private String getCompleteTableName(){
		return this.db.getDatabaseName()+"."+this.getTableName();
	}
}
