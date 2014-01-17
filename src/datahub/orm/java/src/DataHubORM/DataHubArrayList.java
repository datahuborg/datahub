package DataHubORM;

import java.lang.reflect.ParameterizedType;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

import Annotations.Association;
import Annotations.Association.AssociationTypes;
import DataHubResources.Resources;
import DataHubWorkers.DataHubWorker;
import DataHubWorkers.GenericCallback;
import DataHubWorkers.GenericExecutable;

//ArrayList to represent sets connected to a particular 
//table via foreign key
//setup currentModel during model creation
public class DataHubArrayList<T extends DataHubModel> extends ArrayList<T>{
	
	//TODO: throw exceptions if db not set or currentModel not set
	private static DataHubDatabase db;
	
	private DataHubModel currentModel;
	
	private Association association;
	
	private ArrayList<T> tempAdd;
	
	private ArrayList<DataHubModel> tempRemove;
	
	public DataHubArrayList() throws DataHubException{
		/*if(this.foreignKey == null || this.currentModel == null){
			throw new DataHubException("DataHubArrayList must have a foreign key and current model specified!");
		}*/
		tempAdd = new ArrayList<T>();
		tempRemove = new ArrayList<DataHubModel>();
	}
	
	public static void setDatabase(DataHubDatabase database) throws DataHubException{
		//TODO: figure out why this is getting set more than once
		db=database;
		/*if(db == null){
			db = database;
		}else{
			//throw new DataHubException();
		}*/
	}
	public static DataHubDatabase getDatabase(){
		return db;
	}
	private void addItemSQL(DataHubModel data) throws DataHubException{
		String query = getAddItemSQL(data);
		db.query(query);
	}
	//TODO:fix this
	private String getAddItemSQL(DataHubModel data) throws DataHubException{
		//data needs to be saved before it can be added to the collection
		//need to get class that contains this object
		//need to get class of T and then do mappings based on table names
		//check for column annotation and foreign key stuff
		String associateTableName = data.getCompleteTableName();
		String linkingTableName = db.getDatabaseName()+"."+this.association.linkingTable();
		String query = "";
		switch(this.association.associationType()){
			case HasMany:
				query = "update "+associateTableName+" set "+this.association.foreignKey()+"="+this.currentModel.id+" where id="+data.id;
				break;
			case HasAndBelongsToMany:
				int leftVal;
				int rightVal;
				if(this.association.leftTableForeignKey().equals(this.association.foreignKey())){
					leftVal = this.currentModel.id;
					rightVal = data.id;
				}else if(this.association.rightTableForeignKey().equals(this.association.foreignKey())){
					rightVal = this.currentModel.id;
					leftVal = data.id;
				}else{
					throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
				}
				//String update = "update "+linkingTableName+" set "+this.association.leftTableForeignKey()+"="+leftVal+" where "+this.association.rightTableForeignKey()+"="+rightVal;
				String insert = "insert into "+linkingTableName+"("+this.association.leftTableForeignKey()+","+this.association.rightTableForeignKey()+")"+
						" select "+leftVal+","+rightVal+" where not exists (select 1 from "+linkingTableName+" where "+this.association.leftTableForeignKey()+"="+
						leftVal+" AND "+this.association.rightTableForeignKey()+"="+rightVal+")";
				query = insert;
				break;
			default:
				throw new DataHubException("Invalid association type for DataHubArrayList!");
		}
		return query;
	}
	private void removeItemSQL(DataHubModel data) throws DataHubException{
		String query = getRemoveItemSQL(data);
		db.query(query);
	}
	private String getRemoveItemSQL(DataHubModel data) throws DataHubException{
		String associateTableName = data.getCompleteTableName();
		String query = "";
		switch(this.association.associationType()){
			case HasMany:
				query = "update "+associateTableName+" set "+this.association.foreignKey()+"= NULL "+"where id="+data.id;
				break;
			case HasAndBelongsToMany:
				int leftVal;
				int rightVal;
				if(this.association.leftTableForeignKey().equals(this.association.foreignKey())){
					leftVal = this.currentModel.id;
					rightVal = data.id;
				}else if(this.association.rightTableForeignKey().equals(this.association.foreignKey())){
					rightVal = this.currentModel.id;
					leftVal = data.id;
				}else{
					throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
				}
				query = "delete from "+db.getDatabaseName()+"."+this.association.linkingTable()+" where "+this.association.leftTableForeignKey()+"="+leftVal+" AND "+this.association.rightTableForeignKey()+"="+rightVal;
				break;
			default:
				throw new DataHubException("Invalid association type for DataHubArrayList!");
		}
		return query;
	}
	//TODO:fix this
	@Override
	public boolean add(T data){
		if(!this.contains(data)){
			this.tempAdd.add(data);
			this.tempRemove.remove(data);
			return super.add(data);
		}
		return false;
	}
	
	@Override
	public boolean remove(Object o){
		if(DataHubConverter.isModelSubclass(o.getClass())){
			DataHubModel m = (DataHubModel) o;
			return this.tempRemove.add(m) && super.remove(o) && this.tempAdd.remove(o);
		}
		return false;
	}
	@Override
	public void clear(){
		for(DataHubModel m:this){
			this.remove(m);
		}
	}
	public void setCurrentModel(DataHubModel m) throws DataHubException{
		//model can only be set once for life of the object to ensure consistency in operation
		if(this.currentModel != null){
			throw new DataHubException("Model already set for DataHubArrayList");
		}else{
			this.currentModel = m;
		}
	}
	public void setAssociation(Association a) throws DataHubException{
		//foreignkey can only be set once for life of the object to ensure consistency in operation
		if(this.association != null){
			throw new DataHubException("Association already set for DataHubArrayList");
		}else{
			this.association = a;
		}
	}
	public void populateAsync(final GenericCallback<DataHubArrayList<T>> callback) throws DataHubException{
		final DataHubArrayList<T> object = (DataHubArrayList<T>) this;
		DataHubWorker<DataHubArrayList<T>> dhw = new DataHubWorker<DataHubArrayList<T>>(new GenericExecutable<DataHubArrayList<T>>(){

			//TODO:fix this
			@Override
			public DataHubArrayList<T> call() {
				try {
					populate();
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				return object;
			}}, callback);
		dhw.execute();
	}
	public void saveAsync(final GenericCallback<DataHubArrayList<T>> callback) throws DataHubException{
		final DataHubArrayList<T> object = (DataHubArrayList<T>) this;
		DataHubWorker<DataHubArrayList<T>> dhw = new DataHubWorker<DataHubArrayList<T>>(new GenericExecutable<DataHubArrayList<T>>(){

			//TODO:fix this
			@Override
			public DataHubArrayList<T> call() {
				try {
					save();
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				return object;
			}}, callback);
		dhw.execute();
	}
	public void populate() throws DataHubException{
		populate(DataHubDatabase.MAX_LOAD_RECURSION_DEPTH, new ConcurrentHashMap<String,Object>(),new ConcurrentHashMap<String,Object>());
	}
	public void save() throws DataHubException{
		String query = save(DataHubDatabase.MAX_SAVE_RECURSION_DEPTH, new ConcurrentHashMap<String,Object>());
		db.query(query);
	}
	String save(int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache) throws DataHubException{
		if(recursionDepthLimit <= 0){
			return "";
		}
		ArrayList<DataHubModel> tempAddClone = (ArrayList<DataHubModel>) this.tempAdd.clone();
		ArrayList<DataHubModel> tempRemoveClone = (ArrayList<DataHubModel>) this.tempRemove.clone();
		ArrayList<String> queries = new ArrayList<String>();
		for(DataHubModel element:tempAddClone){
			//need to save new model at least once
			String queryElement = element.save(Math.max(1, recursionDepthLimit-1),localCache);
			String addItemSql = this.getAddItemSQL(element);
			queries.add(queryElement);
			queries.add(addItemSql);
		}
		for(DataHubModel element:tempRemoveClone){
			//need to save new model at least once
			String queryElement = element.save(Math.max(1, recursionDepthLimit-1),localCache);
			String removeItemSql = this.getRemoveItemSQL(element);
			queries.add(queryElement);
			queries.add(removeItemSql);
		}
		reset();
		return Resources.concatenate(queries, ";");
	}
	private void reset(){
		this.tempAdd = new ArrayList<T>();
		this.tempRemove = new ArrayList<DataHubModel>();
	}
	Class<T> getAssociatedModelClass(){
		return ((Class<T>)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]);
	}
	String getPopulateQuery(){
		String query = "";
		String tableName = currentModel.getCompleteTableName();
		//join on table provided by class
		//possibly only select relevant model fields
		try{
			T newInstance = (T) ((Class)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]).newInstance();
			String newTableName = newInstance.getCompleteTableName();
			//TODO: fix select *
			//String query = "select "+"*"+" from "+tableName+", "+newTableName+" where "+newTableName+"."+this.foreignKey+" = "+currentModel.id;
			switch(this.association.associationType()){
				case HasMany:
					query = "select "+"*"+" from "+newTableName+" where "+newTableName+"."+this.association.foreignKey()+" = "+currentModel.id;
					break;
				case HasAndBelongsToMany:
					String linkTableSelectKey;
					String linkTableSearchKey;
					if(this.association.leftTableForeignKey().equals(this.association.foreignKey())){
						linkTableSelectKey = this.association.rightTableForeignKey();
						linkTableSearchKey = this.association.leftTableForeignKey();
					}else if(this.association.rightTableForeignKey().equals(this.association.foreignKey())){
						linkTableSelectKey = this.association.leftTableForeignKey();
						linkTableSearchKey = this.association.rightTableForeignKey();
					}else{
						throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
					}
					String query1 = "select ("+linkTableSelectKey+") from "+db.getDatabaseName()+"."+this.association.linkingTable()+" where "+linkTableSearchKey+"="+this.currentModel.id;
					//TODO:fix this
					query = "select * from "+newTableName+" where id in("+query1+")";
					//System.out.println(query);
					break;
				default:
					throw new DataHubException("Invalid association type for DataHubArrayList!");
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		return query;
	}
	void addInverseQueries(ConcurrentHashMap<String,Object> objectHash) throws InstantiationException, IllegalAccessException, DataHubException{
		for(DataHubModel m:this){
			String newTableName = this.currentModel.getCompleteTableName();
			//TODO: fix select *
			//String query = "select "+"*"+" from "+tableName+", "+newTableName+" where "+newTableName+"."+this.foreignKey+" = "+currentModel.id;
			String query = "";
			switch(this.association.associationType()){
				case HasMany:
					break;
				default:
					throw new DataHubException("Invalid association type for DataHubArrayList!");
			}
			//objectHash.put(key, value)
		}
	}
	//add query this set methods
	void populate(int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache,ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		if(this.association == null || this.currentModel == null){
			throw new DataHubException("Foreign Key and Current Model must be specified in DataHubArrayList");
		}
		if(recursionDepthLimit <= 0){
			return;
		}
		String tableName = currentModel.getCompleteTableName();
		//join on table provided by class
		//possibly only select relevant model fields
		try{
			T newInstance = (T) ((Class)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]).newInstance();
			String query = getPopulateQuery();
			ArrayList<T> data;
			if(objectHash!=null && objectHash.contains(query)){
				data = (ArrayList<T>) objectHash.get(query);
			}else{
				data = (ArrayList<T>) getDatabase().query(query, newInstance.getClass(),recursionDepthLimit,localCache,objectHash);
			}
			this.addAll(data);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}
