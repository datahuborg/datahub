package DataHubORM;

import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
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
	public static void setDatabase(Database database) throws DataHubException{
		//TODO: figure out why this is getting set more than once
		db=database;
		/*if(db == null){
			db = database;
		}else{
			//throw new DataHubException();
		}*/
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
				//System.out.println(query);
			}else{
				query = "UPDATE "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.id;
			}
			DHQueryResult dhqr = db.dbQuery(query);
			//System.out.println(dhqr);
			updateModel();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public void destroy(){
		try{
			String query = "DELETE FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.id;
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			//System.out.println(query);
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
		ArrayList<String> keyVal = new ArrayList<String>();
		for(String field:query.keySet()){
			if(Resources.hasField(this.getClass(), field)){
				String val = Resources.objectToSQL(query.get(field));
				keyVal.add(field+"="+val);
			}			
		}
		return converToSQLAndConcatenate(keyVal,"AND");
	}
	private String generateSQLRep(){
		return generateSQLRep(",");
	}
	private String generateSQLRep(String linkSymbol){
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		ArrayList<String> fieldData = new ArrayList<String>();
		for(String field:currentModel.keySet()){
			if(field!="id"){
				String val = Resources.getFieldStringRep(this,field);
				fieldData.add(val);
			}
		}
		return converToSQLAndConcatenate(fieldData,linkSymbol);
	}
	private <Q> String converToSQLAndConcatenate(Iterable<Q> i, String linkSymbol){
		String out = "";
		for(Q object: i){
			String objStr = Resources.objectToSQL(i);
			out+=objStr;
			if(i.iterator().hasNext()){
				out+=" "+linkSymbol+" ";
			}
		}
		return out;
	}
	private String getFieldNames(){
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		return converToSQLAndConcatenate(currentModel.keySet(),",");
	}
	private String getFieldValues(){
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		ArrayList<String> fieldData = new ArrayList<String>();
		for(String field:currentModel.keySet()){
			fieldData.add(Resources.getFieldStringRep(this,field));
		}
		return converToSQLAndConcatenate(fieldData,",");
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
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ this.getCompleteTableName()+" WHERE "+generateSQLRep("AND");
		DHQueryResult dhqr = this.db.dbQuery(query);
		updateNewModel(dhqr,0,(T)this);
	}
	private void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate){
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		HashMap<String,String> columnToField = new HashMap<String,String>();
		for(Field f: this.getClass().getDeclaredFields()){
			if(f.isAnnotationPresent(column.class)){
				columnToField.put(f.getAnnotation(column.class).name(), f.getName());
			}
		}
		if(table.rows.size() > 0){
			DHRow row = table.rows.get(rowNumber);
			List<DHField> fields = schema.getFields();
			for(int j = 0; j < fields.size(); j++){
				DHField f = fields.get(j);
				DHCell v = row.getCells().get(j);
				try{
					//TODO: change from getting field name directly to getting annotations
					//from annotation get field
					if(columnToField.containsKey(f.name)){
						String fieldName = columnToField.get(f.name);
						Field f1 = this.getClass().getField(fieldName);
						//specifically set id
						if(f.name.equals("id")){
							objectToUpdate.id = (int)Resources.convert(v.value, Integer.TYPE);
						}
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
