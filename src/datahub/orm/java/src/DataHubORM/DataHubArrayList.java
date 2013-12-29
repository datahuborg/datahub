package DataHubORM;

import java.lang.reflect.ParameterizedType;
import java.util.ArrayList;

//ArrayList to represent sets connected to a particular 
//table via foreign key
//setup currentModel during model creation
public class DataHubArrayList<T extends Model> extends ArrayList<T>{
	
	//TODO: throw exceptions if db not set or currentModel not set
	private static Database db;
	
	private Model currentModel;
	
	private String foreignKey;
	
	
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
	protected Class<T> getAssociatedModelClass(){
		return ((Class<T>)((ParameterizedType)this.getClass().getGenericSuperclass()).getActualTypeArguments()[0]);
	}
	//add query this set methods
	protected void populate(int recursionDepthLimit){
		if(recursionDepthLimit == 0){
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
			ArrayList<T> data = (ArrayList<T>) getDatabase().query(query, newInstance.getClass(),recursionDepthLimit-1);
			this.addAll(data);
		}catch(Exception e){
			e.printStackTrace();
		}
		//currentModel.getDatabase().dbQuery(query)
	}
	public void populate(){
		populate(Database.MAX_RECURSION_DEPTH);
	}
}
