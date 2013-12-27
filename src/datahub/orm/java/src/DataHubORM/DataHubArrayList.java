package DataHubORM;

import java.lang.reflect.ParameterizedType;
import java.util.ArrayList;

//ArrayList to represent sets connected to a particular 
//table via foreign key
//setup currentModel during model creation
public class DataHubArrayList<T extends Model> extends ArrayList<T>{
	
	private static Database db;
	
	private Model currentModel;
	
	
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
	
	@Override
	public boolean add(T data){
		//need to get class that contains this object
		//need to get class of T and then do mappings based on table names
		//check for column annotation and foreign key stuff
		return super.add(data);
	}
	
	@Override
	public boolean remove(Object o){
		return super.remove(o);
		
	}
	@Override
	public void clear(){
		super.clear();
	}
	public void setCurrentModel(Model m) throws DataHubException{
		if(this.currentModel != null){
			throw new DataHubException("Model already set for DataHubArrayList");
		}else{
			this.currentModel = m;
		}
	}
	//add query this set methods
	public void populate(){
		String tableName = currentModel.getCompleteTableName();
		//join on table provided by class
		//possibly only select relevant model fields
		try{
			T newInstance = (T) ((Class)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]).newInstance();
			//TODO: fix select *
			String query = "select "+"*"+" from "+tableName+", "+newInstance.getCompleteTableName()+" where "+tableName+".id = "+currentModel.id;
			ArrayList<T> data = (ArrayList<T>) getDatabase().query(query, newInstance);
			this.addAll(data);
		}catch(Exception e){
			e.printStackTrace();
		}
		//currentModel.getDatabase().dbQuery(query)
	}
}
