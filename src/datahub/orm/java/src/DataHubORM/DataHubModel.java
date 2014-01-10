package DataHubORM;

import java.lang.annotation.Annotation;
import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

import Workers.DataHubWorker;
import Workers.GenericCallback;
import Workers.GenericExecutable;

import datahub.DHCell;
import datahub.DHData;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;
import datahub.DHType;

import Annotations.Association;
import Annotations.IntegerField;
import Annotations.Association.AssociationType;
import Annotations.Column;
import Annotations.Column.Index;
import Annotations.Table;
import DataHubResources.Resources;
import Examples.TestModel;

@Table(name="")
public class DataHubModel<T extends DataHubModel>{
	
	
	private static DataHubDatabase db;
	
	@Column(name="id")
	@IntegerField(Serial=true)
	public int id;
	
	public DataHubModel() throws DataHubException{
		if(db==null){
			throw new DataHubException("Database for model class must be set before any models can be created!");
		}
		this.id = 0;
		for(Field f: this.getClass().getFields()){
			if(DataHubConverter.isDataHubArrayListSubclass(f.getType()) && DataHubConverter.hasAssociation(f)){
				try{
					Association a = f.getAnnotation(Association.class);
					DataHubArrayList d = (DataHubArrayList) f.getType().newInstance();
					d.setCurrentModel(this);
					d.setAssociation(a);
					Resources.setField(this, f.getName(), d);
				}catch(Exception e){
					
				}
			}
		}
	}
	public static void setDatabase(DataHubDatabase database) throws DataHubException{
		//TODO: figure out why this is getting set more than once
		db=database;
		/*if(db == null){
			db = database;
		}else{
			throw new DataHubException("Database can only be set once for the Model Class!");
		}*/
	}
	public static DataHubDatabase getDatabase(){
		return db;
	}
	public void saveAsync(final GenericCallback<T> callback) throws DataHubException{
		final T object = (T) this;
		DataHubWorker<T> dhw = new DataHubWorker<T>(new GenericExecutable<T>(){

			@Override
			public T call() {
				save();
				return object;
			}}, callback);
		dhw.execute();
	}
	public void destroyAsync(final GenericCallback<Void> callback) throws DataHubException{
		DataHubWorker<Void> dhw = new DataHubWorker<Void>(new GenericExecutable<Void>(){

			@Override
			public Void call() {
				destroy();
				return null;
			}}, callback);
		dhw.execute();
	}
	public synchronized void save(){
		//db.hitCount = 0;
		//db.missCount = 0;
		//System.out.println("before save");
		String query = this.save(DataHubDatabase.MAX_SAVE_RECURSION_DEPTH, new ConcurrentHashMap<String,Object>(), new ArrayList<Class>());
		getDatabase().query(query);
		updateModel(DataHubDatabase.MAX_LOAD_RECURSION_DEPTH,new ConcurrentHashMap<String,Object>());
		//System.out.println("after save");
	}
	protected String save(int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache, ArrayList<Class> modelsAlreadySaved){
		//System.out.println(modelsAlreadySaved);
		//System.out.println(this.getClass());
		if(recursionDepthLimit <= 0 || modelsAlreadySaved.contains(this.getClass())){
			//System.out.println("broke"+modelsAlreadySaved.contains(this.getClass()));
			return "";
		}
		ArrayList<String> queries = new ArrayList<String>();
		try{
			String query = "";
			//fix this
			if(!this.validId()){
				query = "INSERT INTO "+this.getCompleteTableName()+"("+this.getTableBasicFieldNames()+")"+" VALUES( "+getBasicFieldValues()+")";
				//System.out.println(query);
			}else{
				query = "UPDATE "+this.getCompleteTableName()+" SET "+generateSQLRep()+" WHERE "+"id="+this.id;
			}
			//System.out.println(query);
			//just make query no recursion
			//getDatabase().query(query);
			
			if(!this.validId()){
				getDatabase().query(query);
				//get new id
				updateModelId(recursionDepthLimit,localCache);
			}else{
				queries.add(query);
			}
			
			//update already saved models
			modelsAlreadySaved.add(this.getClass());
			
			//recursively save all fields
			for(Field f:this.getClass().getFields()){
				if(this.hasAssociation(f.getName())){
					Object o = f.get(this);
					if(o != null){
						if(DataHubConverter.isModelSubclass(f.getType())){
							DataHubModel m = (DataHubModel) o;
							//TODO: fix this
							Association a = f.getAnnotation(Association.class);
							if(a.associationType() == AssociationType.BelongsTo){
								//System.out.println("updating");
								String associateTableName = this.getCompleteTableName();
								String queryBelongsTo = "UPDATE "+associateTableName+" SET "+a.foreignKey()+"="+m.id+" WHERE id="+this.id;
								//getDatabase().query(queryBelongsTo);
								queries.add(queryBelongsTo);
							}
							if(a.associationType() == AssociationType.HasOne){
								String associateTableName = m.getCompleteTableName();
								String queryHasOne = "UPDATE "+associateTableName+" SET "+a.foreignKey()+"="+m.id+" WHERE id="+this.id;
								//getDatabase().query(queryHasOne);
								queries.add(queryHasOne);
							}
							//System.out.println(m);
							String otherQueries = m.save(recursionDepthLimit-1,localCache,modelsAlreadySaved);
							queries.add(otherQueries);
						}
						//has many or HABTM relationship
						if(DataHubConverter.isDataHubArrayListSubclass(f.getType())){
							DataHubArrayList d = (DataHubArrayList) o;
							String otherQueries = d.save(recursionDepthLimit-1,localCache,modelsAlreadySaved);
							queries.add(otherQueries);
						}
					}
				}
			}
			//updateModel(recursionDepthLimit,localCache);
		}catch(Exception e){
			e.printStackTrace();
		}
		return Resources.concatenate(queries, ";");
	}
	public synchronized void destroy(){
		try{
			String query = "DELETE FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.id;
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			//System.out.println(query);
			getDatabase().query(query);
			//System.out.println(getDatabase().query("SELECT * FROM "+this.getCompleteTableName()+" WHERE "+"id="+this.id, this.getClass()));
			//possibly garbage collect object
			//recursively save all fields
			
			//TODO: supporty cascading delete, but doing it in table definition so that server does it
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public void allAsync(final GenericCallback<ArrayList<T>> callback) throws DataHubException{
		DataHubWorker<ArrayList<T>> dhw = new DataHubWorker<ArrayList<T>>(new GenericExecutable<ArrayList<T>>(){

			@Override
			public ArrayList<T> call() {
				return all();
			}}, callback);
		dhw.execute();
	}
	public void findAll(final HashMap<String,Object> params,final GenericCallback<ArrayList<T>> callback) throws DataHubException{
		DataHubWorker<ArrayList<T>> dhw = new DataHubWorker<ArrayList<T>>(new GenericExecutable<ArrayList<T>>(){

			@Override
			public ArrayList<T> call() {
				try {
					return findAll(params);
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					return null;
				}
			}}, callback);
		dhw.execute();
	}
	public void findOne(final HashMap<String,Object> params,final GenericCallback<T> callback) throws DataHubException{
		DataHubWorker<T> dhw = new DataHubWorker<T>(new GenericExecutable<T>(){

			@Override
			public T call() {
				try {
					return findOne(params);
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					return null;
				}
			}}, callback);
		dhw.execute();
	}
	public ArrayList<T> all(){
		String query = "select * FROM "+this.getCompleteTableName();
		return (ArrayList<T>) getDatabase().query(query, this.getClass());
	}
	public ArrayList<T> findAll(HashMap<String,Object> params) throws DataHubException{
		if(params.size() == 0){
			return new ArrayList<T>();
		}
		//TODO: querying by related object
		//Ideas: 1) if we get a model object then see if there is an association between that object's class
		//and this class 2) if so use the association type to do the appropriate queries 3) if not throw an
		//invalid query exception because it does not make sense to query a model using a related object
		//if there is no association
		//String query = "select * FROM "+this.getCompleteTableName()+" WHERE "+ queryToSQL(params);
		String query = queryToSQL(params);
		return (ArrayList<T>) getDatabase().query(query, this.getClass());
	}
	public T findOne(HashMap<String,Object> params) throws DataHubException{
		//TODO: querying by related object
		if(params.size() != 0){
			String query = queryToSQL(params) +" LIMIT 1";
			ArrayList<T> data = (ArrayList<T>) getDatabase().query(query,this.getClass());
			//System.out.println(data);
			if(data.size() > 0){
				return (T) getDatabase().query(query,this.getClass()).get(0);
			}
		}
		return null; 
	}
	public synchronized void findOnePoll(int interval, HashMap<String,Object> params, final GenericCallback<T> callback){
		
	}
	public synchronized void findAllPoll(int interval, HashMap<String,Object> params, final GenericCallback<T> callback){
		
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
	private boolean hasAssociation(String name){
		boolean out = false;
		try{
			Field f = this.getClass().getField(name);
			if(DataHubConverter.hasAssociation(f)){
				out= true;
			}
		}catch(Exception e){
			
		}
		return out;
	}
	private String queryToSQL(HashMap<String,Object> query) throws DataHubException{
		ArrayList<String> keyVal = new ArrayList<String>();
		String tables = this.getCompleteTableName();
		for(String field:query.keySet()){
			if(hasFieldAndColumnBasic(field)){//also check if has column annotation
				String val = Resources.objectToSQL(query.get(field));
				keyVal.add(this.getCompleteTableName()+"."+field+"="+val);
				continue;
			}
			Object o = query.get(field);
			HashMap<Field,DHType> fields = DataHubConverter.extractAssociationsFromClass(this.getClass()).get(this.getClass());
			Field match = null;
			for(Field f: fields.keySet()){
				if(DataHubConverter.isModelSubclass(f.getType())){
					if(f.getType() == o.getClass()){
						match = f;
					}
				}
				//add part of query that searches for all records that have the desired object in their list of objects of that type
				//i.e. a model has many users and you want to find all instances of the model that have the specified user in their lists
				//when querying by object and the member type is a DataHubArrayList then provide a normal arraylist with a list
				//of objects that would go into the DataHubArrayList for which you want to find a record whose DataHubArrayList
				//contains those elements
				if(DataHubConverter.isDataHubArrayListSubclass(f.getType())){
					
				}
			}
			if(match!=null){
				Association a = match.getAnnotation(Association.class);
				DataHubModel m;
				if(DataHubConverter.isModelSubclass(o.getClass())){
					m = (DataHubModel) o;
				}else{
					//TODO:fix this
					throw new DataHubException("Errror");
				}
				String newKey = "";
				//System.out.println(a.associationType());
				switch(a.associationType()){
					case HasOne:
						newKey = this.getCompleteTableName()+".id in(select "+a.foreignKey()+" from "+m.getCompleteTableName()+
						" where "+m.getCompleteTableName()+".id="+m.id+")";
						//System.out.println(newKey);
						break;
					case BelongsTo:
						newKey = this.getCompleteTableName()+".id in(select "+this.getCompleteTableName()+".id from "+this.getCompleteTableName()+
						" where "+this.getCompleteTableName()+"."+a.foreignKey()+"="+m.id+")";
						break;
					/*
					case HasMany:
						break;
					case HasAndBelongsToMany:
						String linkTableSelectKey;
						String linkTableSearchKey;
						if(a.leftTableForeignKey().equals(a.foreignKey())){
							linkTableSelectKey = a.rightTableForeignKey();
							linkTableSearchKey = a.leftTableForeignKey();
						}else if(a.rightTableForeignKey().equals(a.foreignKey())){
							linkTableSelectKey = a.leftTableForeignKey();
							linkTableSearchKey = a.rightTableForeignKey();
						}else{
							throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
						}
						String query1 = "select ("+linkTableSelectKey+") from "+db.getDatabaseName()+"."+a.linkingTable()+" where "+linkTableSearchKey+"="+this.id;
						//TODO:fix this
						newKey = this.getCompleteTableName()+".id in("+query1+")";
						break;*/
					default:
						//throw exception
						break;
				}
				keyVal.add(newKey);
			}else{
				throw new DataHubException("No association found in model being queried for "+o.getClass()+"! Cannot perform query!");
			}
		}
		//check to see if tables is not null and whereclause is not null
		String queryStr = "select * from "+tables+" where "+Resources.concatenate(keyVal,"AND");
		//System.out.println(queryStr);
		return queryStr;
	}
	protected String generateSQLRep(){
		return generateSQLRep(",");
	}
	protected String generateSQLRep(String linkSymbol){
		HashMap<Class,HashMap<Field,DHType>> models = DataHubConverter.extractColumnBasicFromClass(this.getClass());
		HashMap<Field,DHType> currentModel = models.get(this.getClass());
		ArrayList<String> fieldData = new ArrayList<String>();
		for(Field f:currentModel.keySet()){
			Column c = f.getAnnotation(Column.class);
			if(c.name().equals("id") && !this.validId()){
				continue;
			}
			try{
				Object o = f.get(this);
				String entry = c.name()+"="+Resources.objectToSQL(o);
				fieldData.add(entry);
			}catch(Exception e){
				
			}
		}
		return Resources.concatenate(fieldData,linkSymbol);
	}
	protected String getTableBasicFieldNames(){
		HashMap<Class,HashMap<Field,DHType>> models = DataHubConverter.extractColumnBasicFromClass(this.getClass());
		HashMap<Field,DHType> currentModel = models.get(this.getClass());
		ArrayList<String> getFieldTableNames = new ArrayList<String>();
		for(Field f: currentModel.keySet()){
			Column c = f.getAnnotation(Column.class);
			if(c.name().equals("id")){
				continue;
			}
			getFieldTableNames.add(c.name());
		}
		return Resources.concatenate(getFieldTableNames,",");
	}
	protected String getBasicFieldValues(){
		HashMap<Class,HashMap<Field,DHType>> models = DataHubConverter.extractColumnBasicFromClass(this.getClass());
		HashMap<Field,DHType> currentModel = models.get(this.getClass());
		//System.out.println(this.getTableName());
		//System.out.println(currentModel);
		ArrayList<String> fieldData = new ArrayList<String>();
		for(Field f: currentModel.keySet()){
			Column c = f.getAnnotation(Column.class);
			if(c.name().equals("id")){
				continue;
			}
			String value = Resources.getFieldStringRep(this, f.getName());
			//System.out.println(value);
			fieldData.add(value);
		}
		return Resources.converToSQLAndConcatenate(fieldData,",");
	}
	public void refreshModel(){
		updateModel(DataHubDatabase.MAX_LOAD_RECURSION_DEPTH,new ConcurrentHashMap<String,Object>());
	}
	private void updateModel(int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache){
		getDatabase().updateModelObject(this,recursionDepthLimit,localCache);
	}
	private void updateModelId(int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache){
		getDatabase().updateModelId(this,recursionDepthLimit,localCache);
	}
	private T newInstance() throws InstantiationException, IllegalAccessException{
		return (T) getClass().newInstance();
	}
	public String getTableName(){
		Table t = this.getClass().getAnnotation(Table.class);
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
			DataHubModel other = (DataHubModel) o;
			String otherSQLRep = other.getCompleteTableName()+other.generateSQLRep();
			String thisSQLRep = this.getCompleteTableName()+this.generateSQLRep();
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
		return this.getCompleteTableName()+this.generateSQLRep();
	}
	public boolean validId(){
		if(this.id <= 0){
			return false;
		}
		return true;
	}
}
