package DataHubORM;

import java.lang.reflect.ParameterizedType;
import java.util.ArrayList;
import java.util.HashMap;

//ArrayList to represent sets connected to a particular 
//table via foreign key
//setup currentModel during model creation
public class DataHubArrayList<T extends Model> extends ArrayList<T>{
	
	//TODO: throw exceptions if db not set or currentModel not set
	private static Database db;
	
	private Model currentModel;
	
	private String foreignKey;
	
	private ArrayList<T> tempAdd;
	
	private ArrayList<Model> tempRemove;
	
	public DataHubArrayList(){
		tempAdd = new ArrayList<T>();
		tempRemove = new ArrayList<Model>();
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
	//TODO:fix this
	private void addItemSQL(Model data){
		//data needs to be saved before it can be added to the collection
		//need to get class that contains this object
		//need to get class of T and then do mappings based on table names
		//check for column annotation and foreign key stuff
		String associateTableName = data.getCompleteTableName();
		String query = "UPDATE "+associateTableName+" SET "+this.foreignKey+"="+this.currentModel.id+" WHERE id="+data.id;
		db.query(query, data.getClass());
	}
	private void removeItemSQL(Model data){
		String associateTableName = data.getCompleteTableName();
		String query = "UPDATE "+associateTableName+" SET "+this.foreignKey+"= NULL "+"WHERE id="+data.id;
		db.query(query, data.getClass());
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
			Model m = (Model) o;
			return this.tempRemove.add(m) && super.remove(o) && this.tempAdd.remove(o);
		}
		return false;
	}
	@Override
	public void clear(){
		for(Model m:this){
			this.remove(m);
		}
	}
	public void setCurrentModel(Model m) throws DataHubException{
		//model can only be set once for life of the object to ensure consistency in operation
		if(this.currentModel != null){
			throw new DataHubException("Model already set for DataHubArrayList");
		}else{
			this.currentModel = m;
		}
	}
	public void setForeignKey(String foreignKey) throws DataHubException{
		//foreignkey can only be set once for life of the object to ensure consistency in operation
		if(this.foreignKey != null){
			throw new DataHubException("ForeignKey already set for DataHubArrayList");
		}else{
			this.foreignKey = foreignKey;
		}
	}
	public void populate(){
		populate(Database.MAX_LOAD_RECURSION_DEPTH);
	}
	public void save(){
		db.resetCache();
		save(Database.MAX_SAVE_RECURSION_DEPTH);
		db.resetCache();
	}
	protected void save(int recursionDepthLimit){
		if(recursionDepthLimit <= 0){
			return;
		}
		ArrayList<Model> tempAddClone = (ArrayList<Model>) this.tempAdd.clone();
		ArrayList<Model> tempRemoveClone = (ArrayList<Model>) this.tempRemove.clone();
		for(Model element:tempAddClone){
			element.save(recursionDepthLimit);
			this.addItemSQL(element);
		}
		for(Model element:tempRemoveClone){
			element.save(recursionDepthLimit);
			this.removeItemSQL(element);
		}
		reset();
	}
	private void reset(){
		this.tempAdd = new ArrayList<T>();
		this.tempRemove = new ArrayList<Model>();
	}
	protected Class<T> getAssociatedModelClass(){
		return ((Class<T>)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]);
	}
	//add query this set methods
	protected void populate(int recursionDepthLimit){
		if(recursionDepthLimit <= 0){
			return;
		}
		String tableName = currentModel.getCompleteTableName();
		//join on table provided by class
		//possibly only select relevant model fields
		try{
			T newInstance = (T) ((Class)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]).newInstance();
			String newTableName = newInstance.getCompleteTableName();
			//TODO: fix select *
			//String query = "select "+"*"+" from "+tableName+", "+newTableName+" where "+newTableName+"."+this.foreignKey+" = "+currentModel.id;
			String query = "select "+"*"+" from "+newTableName+" where "+newTableName+"."+this.foreignKey+" = "+currentModel.id;
			ArrayList<T> data = (ArrayList<T>) getDatabase().query(query, newInstance.getClass(),recursionDepthLimit);
			this.addAll(data);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}
