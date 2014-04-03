package DataHubORM;

import java.lang.reflect.ParameterizedType;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

import DataHubAnnotations.Association;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubResources.Resources;
import DataHubWorkers.DataHubWorker;
import DataHubWorkers.GenericCallback;
import DataHubWorkers.GenericExecutable;

//ArrayList to represent sets connected to a particular 
//table via foreign key
//setup currentModel during model creation
public class DataHubArrayList<T extends DataHubModel> extends ArrayList<T>{
	
	private DataHubModel currentModel;
	
	private Association association;
	
	private ArrayList<T> tempAdd;
	
	private ArrayList<DataHubModel> tempRemove;
	
	public DataHubArrayList() throws DataHubException{
		tempAdd = new ArrayList<T>();
		tempRemove = new ArrayList<DataHubModel>();
	}
	public DataHubDatabase getDatabase() throws DataHubException{
		DataHubDatabase db = null;
		try {
			DataHubDatabase db1 = this.getAssociatedModelClass().newInstance().getDatabase();
			DataHubDatabase db2 = this.currentModel.getDatabase();
			if (db2==null || db1.equals(db2)){
				db=db1;
			}
		} catch(Exception e){
			
		}
		return db;
	}
	private void addItemSQL(DataHubModel data) throws DataHubException{
		String query = getAddItemSQL(data);
		getDatabase().query(query);
	}
	//TODO:fix this
	private String getAddItemSQL(DataHubModel data) throws DataHubException{
		//data needs to be saved before it can be added to the collection
		//need to get class that contains this object
		//need to get class of T and then do mappings based on table names
		//check for column annotation and foreign key stuff
		DataHubModel currentModel = null;
		DataHubModel otherModel  = null;
		try {
			currentModel = this.currentModel.getClass().newInstance();
			otherModel = this.getAssociatedModelClass().newInstance();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String foreignKey = DataHubConverter.AssociationDefaultsHandler.getForeignKey(this.association, currentModel, otherModel);
		String linkingTable = DataHubConverter.AssociationDefaultsHandler.getLinkingTableName(this.association, currentModel, otherModel);
		String leftTableForeignKey = DataHubConverter.AssociationDefaultsHandler.getRightTableForeignKey(this.association, currentModel, otherModel);
		String rightTableForeignKey = DataHubConverter.AssociationDefaultsHandler.getLeftTableForeignKey(this.association, currentModel, otherModel);
		
		String associateTableName = data.getCompleteTableName();
		String linkingTableName = getDatabase().getDatabaseName()+"."+linkingTable;
		String query = "";
		
		switch(this.association.associationType()){
			case HasMany:
				query = "update "+associateTableName+" set "+foreignKey+"="+this.currentModel.id+" where id="+data.id;
				break;
			case HasAndBelongsToMany:
				int leftVal;
				int rightVal;
				if(leftTableForeignKey.equals(foreignKey)){
					leftVal = this.currentModel.id;
					rightVal = data.id;
				}else if(rightTableForeignKey.equals(foreignKey)){
					rightVal = this.currentModel.id;
					leftVal = data.id;
				}else{
					throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
				}
				//String update = "update "+linkingTableName+" set "+this.association.leftTableForeignKey()+"="+leftVal+" where "+this.association.rightTableForeignKey()+"="+rightVal;
				String insert = "insert into "+linkingTableName+"("+leftTableForeignKey+","+rightTableForeignKey+")"+
						" select "+leftVal+","+rightVal+" where not exists (select 1 from "+linkingTableName+" where "+leftTableForeignKey+"="+
						leftVal+" AND "+rightTableForeignKey+"="+rightVal+")";
				query = insert;
				break;
			default:
				throw new DataHubException("Invalid association type for DataHubArrayList!");
		}
		return query;
	}
	private void removeItemSQL(DataHubModel data) throws DataHubException{
		String query = getRemoveItemSQL(data);
		getDatabase().query(query);
	}
	private String getRemoveItemSQL(DataHubModel data) throws DataHubException{
		DataHubModel currentModel = null;
		DataHubModel otherModel  = null;
		try {
			currentModel = this.currentModel.getClass().newInstance();
			otherModel = this.getAssociatedModelClass().newInstance();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String foreignKey = DataHubConverter.AssociationDefaultsHandler.getForeignKey(this.association, currentModel, otherModel);
		String linkingTable = DataHubConverter.AssociationDefaultsHandler.getLinkingTableName(this.association, currentModel, otherModel);
		String leftTableForeignKey = DataHubConverter.AssociationDefaultsHandler.getRightTableForeignKey(this.association, currentModel, otherModel);
		String rightTableForeignKey = DataHubConverter.AssociationDefaultsHandler.getLeftTableForeignKey(this.association, currentModel, otherModel);
		
		String associateTableName = data.getCompleteTableName();
		String query = "";
		String linkingTableName = getDatabase().getDatabaseName()+"."+linkingTable;
		
		switch(this.association.associationType()){
			case HasMany:
				query = "update "+associateTableName+" set "+foreignKey+"= NULL "+"where id="+data.id;
				break;
			case HasAndBelongsToMany:
				int leftVal;
				int rightVal;
				if(leftTableForeignKey.equals(foreignKey)){
					leftVal = this.currentModel.id;
					rightVal = data.id;
				}else if(rightTableForeignKey.equals(foreignKey)){
					rightVal = this.currentModel.id;
					leftVal = data.id;
				}else{
					throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
				}
				query = "delete from "+linkingTableName+" where "+leftTableForeignKey+"="+leftVal+" AND "+rightTableForeignKey+"="+rightVal;
				break;
			default:
				throw new DataHubException("Invalid association type for DataHubArrayList!");
		}
		return query;
	}
	//TODO:implement
	@Override
	public void add(int index, T data){
		
	}
	//TODO:implement
	@Override
	public boolean addAll(Collection<? extends T> c){
		return false;
		
	}
	//TODO:implement
	@Override
	public boolean retainAll(Collection<?> c){
		return false;
	
	}
	//TODO:implement
	@Override
	public T set(int index, T data){
		return data;
		
	}
	//TODO:implement
	@Override
	public void trimToSize(){
		
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
	//TODO:implement
	@Override
	public boolean removeAll(Collection<?> c){
		return false;
	}
	@Override
	public void clear(){
		for(DataHubModel m:this){
			this.remove(m);
		}
	}
	void setCurrentModel(DataHubModel m) throws DataHubException{
		//model can only be set once for life of the object to ensure consistency in operation
		if(this.currentModel != null){
			throw new DataHubException("Model already set for DataHubArrayList");
		}else{
			this.currentModel = m;
		}
	}
	void setAssociation(Association a) throws DataHubException{
		//foreignkey can only be set once for life of the object to ensure consistency in operation
		if(this.association != null){
			throw new DataHubException("Association already set for DataHubArrayList");
		}else{
			this.association = a;
		}
	}
	public void populateAsync(final GenericCallback<DataHubArrayList<T>> succeedCallback, final GenericCallback<DataHubException> failCallback) throws DataHubException{
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
			}}, succeedCallback, failCallback);
		dhw.execute();
	}
	public void populate() throws DataHubException{
		populate(DataHubDatabase.MAX_LOAD_RECURSION_DEPTH, new ConcurrentHashMap<String,Object>(),new ConcurrentHashMap<String,Object>());
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
		DataHubModel currentModel = null;
		DataHubModel otherModel  = null;
		try {
			currentModel = this.currentModel.getClass().newInstance();
			otherModel = this.getAssociatedModelClass().newInstance();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String foreignKey = DataHubConverter.AssociationDefaultsHandler.getForeignKey(this.association, currentModel, otherModel);
		String linkingTable = DataHubConverter.AssociationDefaultsHandler.getLinkingTableName(this.association, currentModel, otherModel);
		String leftTableForeignKey = DataHubConverter.AssociationDefaultsHandler.getRightTableForeignKey(this.association, currentModel, otherModel);
		String rightTableForeignKey = DataHubConverter.AssociationDefaultsHandler.getLeftTableForeignKey(this.association, currentModel, otherModel);
		
		String query = "";
		String tableName = currentModel.getCompleteTableName();
		//join on table provided by class
		//possibly only select relevant model fields
		try{
			//TODO: fix select *
			//String query = "select "+"*"+" from "+tableName+", "+newTableName+" where "+newTableName+"."+this.foreignKey+" = "+currentModel.id;
			switch(this.association.associationType()){
				case HasMany:
					query = "select "+"*"+" from "+otherModel.getCompleteTableName()+" where "+otherModel.getCompleteTableName()+"."+foreignKey+" = "+this.currentModel.id;
					break;
				case HasAndBelongsToMany:
					String linkTableSelectKey;
					String linkTableSearchKey;
					if(leftTableForeignKey.equals(foreignKey)){
						linkTableSelectKey = rightTableForeignKey;
						linkTableSearchKey = leftTableForeignKey;
					}else if(rightTableForeignKey.equals(foreignKey)){
						linkTableSelectKey = leftTableForeignKey;
						linkTableSearchKey = rightTableForeignKey;
					}else{
						throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
					}
					String query1 = "select ("+linkTableSelectKey+") from "+getDatabase().getDatabaseName()+"."+linkingTable+" where "+linkTableSearchKey+"="+this.currentModel.id;
					//TODO:fix this
					query = "select * from "+otherModel.getCompleteTableName()+" where id in("+query1+")";
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
			this.addAllBasic(data);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	void addAllBasic(Collection<? extends T> c){
		super.addAll(c);
	}
}
