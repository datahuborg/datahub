package DataHubORM;

import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.Type;
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
import Annotations.column.Index;
import Annotations.column.RelationType;
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
		for(Field f: this.getClass().getFields()){
			if(DataHubConverter.isDataHubArrayListSubclass(f.getType())){
				try{
					DataHubArrayList d = (DataHubArrayList) f.getType().newInstance();
					d.setCurrentModel(this);
					d.setDatabase(db);
					Resources.setField(this, f.getName(), f.getType().newInstance());
				}catch(Exception e){
					
				}
			}
		}
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
		db.resetCache();
		this.save(Database.MAX_SAVE_RECURSION_DEPTH);
		db.resetCache();
	}
	protected void save(int recursionDepthLimit){
		if(recursionDepthLimit <= 0){
			return;
		}
		try{
			String query = "";
			//fix this
			if(!this.validId()){
				query = "INSERT INTO "+this.getCompleteTableName()+"("+this.getFieldNames()+")"+" VALUES( "+getFieldValues()+")";
				//System.out.println(query);
			}else{
				query = "UPDATE "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.id;
			}
			
			//just make query no recursion
			getDatabase().query(query, this.getClass());
			
			//get new id
			updateModelId();
			
			//recursively save all fields
			for(Field f:this.getClass().getFields()){
				if(this.hasFieldAndColumnWithRelation(f.getName())){
					Object o = f.get(this);
					if(o != null){
						if(DataHubConverter.isModelSubclass(f.getType())){
							Model m = (Model) o;
							m.save(recursionDepthLimit-1);
							//TODO: fix this
							column c = f.getAnnotation(column.class);
							if(c.RelationType() == RelationType.BelongsTo){
								String associateTableName = this.getCompleteTableName();
								String queryBelongsTo = "UPDATE "+associateTableName+" SET "+c.name()+"="+m.id+" WHERE id="+this.id;
								db.query(queryBelongsTo, this.getClass());
							}
							if(c.RelationType() == RelationType.HasOne){
								//TODO:implement
							}
						}
						if(DataHubConverter.isDataHubArrayListSubclass(f.getType())){
							DataHubArrayList d = (DataHubArrayList) o;
							d.save(recursionDepthLimit-1);
						}
					}
				}
			}
			updateModel();
			//System.out.println(this.id);
			//System.out.println(dhqr);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public void destroy(){
		try{
			db.resetCache();
			String query = "DELETE FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.id;
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			//System.out.println(query);
			getDatabase().query(query, this.getClass());
			db.resetCache();
			//System.out.println(getDatabase().query("SELECT * FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.id, this.getClass()));
			//possibly garbage collect object
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public ArrayList<T> all(){
		String query = "select * FROM "+this.getCompleteTableName();
		return (ArrayList<T>) getDatabase().query(query, this.getClass());
	}
	public ArrayList<T> findAll(HashMap<String,Object> params){
		//TODO: queryung by related object
		String query = "select * FROM "+this.getCompleteTableName()+" WHERE "+ queryToSQL(params);
		return (ArrayList<T>) getDatabase().query(query, this.getClass());
	}
	public T findOne(HashMap<String,Object> params){
		//TODO: querying by related object
		String query = "select * FROM "+this.getCompleteTableName()+" WHERE "+ queryToSQL(params) +" LIMIT 1";
		ArrayList<T> data = (ArrayList<T>) getDatabase().query(query,this.getClass());
		//System.out.println(data);
		if(data.size() > 0){
			return (T) getDatabase().query(query,this.getClass()).get(0);
		}
		return null; 
	}
	private boolean hasFieldAndColumnBasic(String name){
		boolean out = false;
		try{
			Field f = this.getClass().getField(name);
			if(DataHubConverter.hasColumnBasic(f)){
				out= true;
			}
		}catch(Exception e){
			
		}
		return out;
	}
	private boolean hasFieldAndColumnWithRelation(String name){
		boolean out = false;
		try{
			Field f = this.getClass().getField(name);
			if(DataHubConverter.hasFieldAndColumnWithRelation(f)){
				out= true;
			}
		}catch(Exception e){
			
		}
		return out;
	}
	private String queryToSQL(HashMap<String,Object> query){
		ArrayList<String> keyVal = new ArrayList<String>();
		for(String field:query.keySet()){
			if(hasFieldAndColumnBasic(field)){//also check if has column annotation
				String val = Resources.objectToSQL(query.get(field));
				keyVal.add(field+"="+val);
			}			
		}
		return Resources.concatenate(keyVal,"AND");
	}
	protected String generateSQLRep(){
		return generateSQLRep(",");
	}
	protected String generateSQLRep(String linkSymbol){
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		ArrayList<String> fieldData = new ArrayList<String>();
		for(String field:currentModel.keySet()){
			if(field!="id"){
				String val = Resources.getFieldStringRep(this,field);
				String entry = field+"="+Resources.objectToSQL(val);
				fieldData.add(entry);
			}
		}
		return Resources.concatenate(fieldData,linkSymbol);
	}
	protected String getFieldNames(){
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		ArrayList<String> fields = new ArrayList<String>();
		/*for(String oldField: currentModel.keySet()){
			String newField = getTableName()+"."+oldField;
			fields.add(newField);
		}
		return Resources.concatenate(fields,",");*/
		return Resources.concatenate(currentModel.keySet(),",");
	}
	protected String getFieldValues(){
		HashMap<String,HashMap<String,DHType>> models = DataHubConverter.extractDataFromClass(this.getClass());
		HashMap<String,DHType> currentModel = models.get(this.getTableName());
		ArrayList<String> fieldData = new ArrayList<String>();
		for(String field:currentModel.keySet()){
			fieldData.add(Resources.getFieldStringRep(this,field));
		}
		return Resources.converToSQLAndConcatenate(fieldData,",");
	}
	private void updateModel(){
		getDatabase().updateModelObject(this);
	}
	private void updateModelId(){
		getDatabase().updateModelId(this);
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
	public String getCompleteTableName(){
		return getDatabase().getDatabaseName()+"."+this.getTableName();
	}
	
	//required for arraylist to work
	@Override
	public boolean equals(Object o){
		if(DataHubConverter.isModelSubclass(o.getClass())){
			Model other = (Model) o;
			String otherSQLRep = other.getCompleteTableName()+"id="+other.id+other.generateSQLRep();
			String thisSQLRep = this.getCompleteTableName()+"id="+this.id+this.generateSQLRep();
			//System.out.println(otherSQLRep);
			//System.out.println(thisSQLRep);
			if(thisSQLRep.equals(otherSQLRep)){
				return true;
			}
		}
		return false;
	}
	@Override
	public String toString(){
		return this.getCompleteTableName()+"id="+this.id+this.generateSQLRep();
	}
	public boolean validId(){
		if(this.id <= 0){
			return false;
		}
		return true;
	}
}
