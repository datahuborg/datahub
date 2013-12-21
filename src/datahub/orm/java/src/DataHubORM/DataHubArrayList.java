package DataHubORM;

import java.util.ArrayList;

//ArrayList to represent sets connected to a particular 
//table via foreign key
//setup currentModel during model creation
public class DataHubArrayList<T extends Model> extends ArrayList<T>{
	
	private Model currentModel;
	
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
}
