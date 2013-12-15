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
	
	private Database db;
	
	@column(name="")
	public int id;

	public Model(){
		
	}
	public void setDatabase(Database db){
		this.db = db;
	}
	public void save(){
		try{
			String query = "";
			//fix this
			if(this.getId() <= 0){
				//query = "INSET INTO "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.getId();
				query = "INSERT INTO "+this.getCompleteTableName()+"(name,description) VALUES('lol','hi')";
				this.db.dbQuery(query);
				this.updateModel();
				query = "UPDATE "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.getId();
			}else{
				query = "UPDATE "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.getId();
			}
			System.out.println(query);
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			DHQueryResult dhqr = this.db.dbQuery(query);
			//updateModel();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public void destroy(){
		try{
			String query = "DELETE FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.getId();
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			this.db.dbQuery(query);
			//possibly garbage collect object
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public ArrayList<T> findAll(){
		
		//non-static implementation (should be static though)
		//get table name
		//get model class name
		//make query to datahub and create new instances 
		ArrayList<T> output = new ArrayList<T>();
		try{
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			output = dhQueryToModel(this.db.dbQuery("select * FROM "+this.getCompleteTableName()));
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	private void setId(int id){
		this.id = id;
	}
	private int getId(){
		return id-48;
	}
	public String generateSQLRep(){
		String out ="";
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		int counter = 0;
		int size = currentModel.keySet().size();
		for(String field:currentModel.keySet()){
			counter++;
			if(field!="id"){
				String val = "";
				try{
					Object o = this.getClass().getField(field).get(this);
					if(o.getClass().equals(String.class)){
						val = "'"+o.toString()+"'";
					}else{
						val = o.toString();
					}
				}catch(Exception e){
					
				}
				out+=field+"="+val;
				if(counter < size){
					out+=",";
				}
			}
		}
		return out;
	}
	public String getFieldNames(){
		String out ="";
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		return out;
	}
	public String getFieldValues(){
		String out ="";
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
			newObj.setDatabase(this.db);
			updateNewModel(dhqr, i,newObj);
			output.add(newObj);
		}
		return output;
	}
	private void updateModel(){
		//worry about casting issues here
		String query = "SELECT * FROM "+ this.getCompleteTableName()+" WHERE  id="+this.getId();
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
				
				//set internal id
				if(f.name.equals("id")){
					setId((int)Resources.convert(v.value, Integer.TYPE));
				}
				//maybe move this somewhere
				try{
					Field f1 = this.getClass().getField(f.name);
					
					if(f1.isAnnotationPresent(column.class)){
						Resources.setField(objectToUpdate, f.name, v.value);
					}
				}catch(Exception e){
					
				}
			}
		}
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
	private String getCompleteTableName(){
		return this.db.getDatabaseName()+"."+this.getTableName();
	}
}
