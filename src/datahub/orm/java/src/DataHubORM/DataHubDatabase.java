package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

import org.apache.thrift.TException;


import datahub.DHCell;
import datahub.DHData;
import datahub.DHException;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;

import Annotations.Association;
import Annotations.Association.AssociationTypes;
import Annotations.Association.LoadTypes;
import Annotations.Column;
import Annotations.Database;
import Annotations.Column.Index;
import Configurations.DataHubCache;
import Configurations.DataHubConsistencySpecifier;
import DataHubAccount.DataHubAccount;
import DataHubResources.Resources;
import DataHubWorkers.DataHubWorker;
import DataHubWorkers.GenericCallback;
import DataHubWorkers.GenericExecutable;
import DataHubWorkers.DataHubWorker.DataHubWorkerMode;

@Database(name="")
public class DataHubDatabase {
	//TODO: issue with stale objects on same system, could keep track of stale objects and update all of them
	
	public enum DatabaseEngine{Postgres};
	
	protected static int MAX_LOAD_RECURSION_DEPTH = 100;
	
	//prevent do unnecessary saves
	protected static int MAX_SAVE_RECURSION_DEPTH = 2;
	
	private DataHubClient dhc;
	
	private DatabaseEngine databaseEngine;
	
	private DataHubWorkerMode dataHubWorkerMode;
	
	public DataHubDatabase(){
		this.dataHubWorkerMode = DataHubWorkerMode.Normal;
		this.instantiateAndSetup();
	}
	public synchronized void setDataHubAccount(DataHubAccount dha){
		this.dhc = new DataHubClient(dha);
	}
	public synchronized void setDataHubWorkerMode(DataHubWorkerMode dataHubWorkerMode){
		this.dataHubWorkerMode = dataHubWorkerMode;
	}
	public synchronized DataHubWorkerMode getDataHubWorkerMode(){
		return dataHubWorkerMode;
	}
	public synchronized void connect() throws DataHubException{
		try {
			dhc.connect(this);
		} catch (Exception e){
			//fix this
			e.printStackTrace();
			throw new DataHubException("Cannot connect to database!");
		}
	}
	public synchronized void clearAndReCreate() throws DataHubException{
		//clear database
		String clearDB = "drop schema "+this.getDatabaseName()+" cascade;";
		
		//re-create database from scratch
		String createDB = "create schema "+this.getDatabaseName()+";";
		String database = DataHubConverter.convertDBToSQLSchemaString(this.getClass());
		String overallQuery = clearDB+createDB+database;
		this.query(overallQuery);
	}
	public synchronized void sync() throws DataHubException{
		//TODO: get better syncing
		throw new DataHubException("Not implemented!");
	}
	public synchronized boolean isConnected(){
		return dhc.isConnected();
	}
	public void connectAsync(final GenericCallback<Void> succeedCallback, final GenericCallback<DataHubException> failCallback) throws DataHubException{
		DataHubWorker<Void> dhw = new DataHubWorker<Void>(new GenericExecutable<Void>(){

			@Override
			public Void call() {
				try {
					connect();
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				return null;
			}},new GenericCallback<Void>(){

				@Override
				public void call(Void data) throws DataHubException {
					if(isConnected()){
						succeedCallback.call(data);
					}else{
						failCallback.call(new DataHubException("Cannot connect to database!"));
					}
					
				}},failCallback, dataHubWorkerMode);
		dhw.execute();
	}
	public synchronized void disconnect(){
		dhc.disconnect();
	}
	public void disconnectAsync(final GenericCallback<Void> succeedCallback, final GenericCallback<DataHubException> failCallback) throws DataHubException{
		DataHubWorker<Void> dhw = new DataHubWorker<Void>(new GenericExecutable<Void>(){

			@Override
			public Void call() {
				disconnect();
				return null;
			}},new GenericCallback<Void>(){

				@Override
				public void call(Void data) throws DataHubException {
					if(!isConnected()){
						succeedCallback.call(data);
					}else{
						throw new DataHubException("Cannot connect to database!");
					}
					
				}}, failCallback, dataHubWorkerMode);
		dhw.execute();
	}
	private void instantiateAndSetup(){
		//System.out.println("called");
		ArrayList<Field> fields = DataHubConverter.findModels(this.getClass());
		try{
			DataHubModel.setDatabase(this);
			DataHubArrayList.setDatabase(this);
		}catch(Exception e){
			e.printStackTrace();
		}
		for(Field f:fields){
			Resources.setField(this,f.getName(), Resources.fieldToInstance(f));
		}
	}
	public synchronized String getDatabaseName(){
		Database d = this.getClass().getAnnotation(Database.class);
		if(d != null){
			return d.name();
		}
		return null;
	}
	/*public <T extends Model> ArrayList<T> insert(T object){
		
	}
	public <T extends Model> ArrayList<T> update(T object){
		
	}
	public <T extends Model> ArrayList<T> select(T object, HashMap<String,Object> queryParams){
		
	}*/
	/*TO BE REMOVED*/
	public static int hitCount = 0;
	public static int missCount = 0;
	public static int otherCount = 0;
	private String filter(String tentative, ConcurrentHashMap<String,Object> obj){
		for(String key:obj.keySet()){
			//System.out.println("key"+key);
			//System.out.println("tentative"+tentative);
			if(key.contains(tentative) || tentative.contains(key)){
				//System.out.println(key);
				return key;
			}
		}
		return null;
	}
	public void resetStats(){
		hitCount=0;
		missCount=0;
		otherCount=0;
	}
	public void printStats(){
		System.out.println("hits"+hitCount);
		System.out.println("misses"+missCount);
		System.out.println("other"+otherCount);
	}
	public DHQueryResult dbQuery(String query){
		return dhc.dbQuery(query);
	}
	/*TO BE REMOVED*/
	private DHQueryResult dbQuery(String query, ConcurrentHashMap<String,Object> localCache){
		//System.out.println(query);
		//System.out.println(dhc.dbQuery(query));
		if(query.toLowerCase().startsWith("select * from")){
			if(localCache.containsKey(query)){
				//System.out.println(query);
				hitCount+=1;
				return (DHQueryResult) localCache.get(query);
			}else{
				//System.out.println(localCache.keySet());
				//System.out.println(query);
				missCount+=1;
				System.out.println(query);
				//System.out.println("network");
				DHQueryResult out = dhc.dbQuery(query);
				localCache.put(query, out);
				return out;
			}
		}else{
			otherCount+=1;
			return dhc.dbQuery(query);
		}
		//return dhc.dbQuery(query);
	}
	void query(String query){
		if(!query.equals("") && query!=null){
			this.dbQuery(query, new ConcurrentHashMap<String,Object>());
		}
	}
	<T extends DataHubModel> ArrayList<T> query(String query, Class<T> modelClass, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash){
		ArrayList<T> output = new ArrayList<T>();
		if(recursionDepthLimit <= 0){
			return output;
		}
		//non-static implementation (should be static though)
		//get table name
		//get model class name
		//make query to datahub and create new instances 
		try{
			//System.out.println(this.db.dbQuery("select * FROM "+this.db.getDatabaseName()+"."+this.getTableName()));
			//System.out.println(this.dbQuery(query));
			/*if(query.toLowerCase().startsWith("select * from")){
				if(localCache.containsKey(query)){
					//System.out.println(query);
					hitCount+=1;
					return (ArrayList<T>) localCache.get(query);
				}else{
					//System.out.println(localCache.keySet());
					//System.out.println(query);
					missCount+=1;
					//System.out.println(query);
					//System.out.println("network");
					output = dhQueryToModel(this.dbQuery(query, localCache), modelClass,recursionDepthLimit-1, localCache);
					localCache.put(query, output);
					return output;
				}
			}else{
				otherCount+=1;
				return dhQueryToModel(this.dbQuery(query, localCache), modelClass,recursionDepthLimit-1, localCache);
			}*/
			output = dhQueryToModel(this.dbQuery(query, localCache), modelClass,recursionDepthLimit-1, localCache, objectHash);
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	
	<T extends DataHubModel> void updateModelObject(T model, int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache,ConcurrentHashMap<String,Object> objectHash){
		updateNewModel(getModelBasicDHQuerResult(model, localCache), 0, model, recursionDepthLimit, localCache,objectHash);
	}
	<T extends DataHubModel> void updateModelId(T model){
		updateNewModel(getModelBasicDHQuerResult(model), 0, model,1, null, null, true, null);
	}
	<T extends DataHubModel> void updateModelObjectField(String fieldName, T model, int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		if(Resources.hasField(model.getClass(), fieldName)){
			ArrayList<String> fields = new ArrayList<String>();
			fields.add(fieldName);
			updateNewModel(getModelBasicDHQuerResult(model, localCache), 0, model,recursionDepthLimit, localCache, fields, false, objectHash);
		}else{
			throw new DataHubException("Model: "+this.getClass().getCanonicalName()+" has no field: "+fieldName+". Cannot refresh field!");
		}
	}
	public <T extends DataHubModel> ArrayList<T> query(String query, Class<T> modelClass){
		return query(query,modelClass,DataHubDatabase.MAX_LOAD_RECURSION_DEPTH, new ConcurrentHashMap<String,Object> (),new ConcurrentHashMap<String,Object> ());
	}
	private <T extends DataHubModel> DHQueryResult getModelBasicDHQuerResult(T model){
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateQuerySQLRep();
		//System.out.println(query);
		DHQueryResult dhqr = this.dbQuery(query);
		return dhqr;
	}
	private <T extends DataHubModel> DHQueryResult getModelBasicDHQuerResult(T model, ConcurrentHashMap<String,Object> localCache){
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateQuerySQLRep();
		//System.out.println(query);
		DHQueryResult dhqr = this.dbQuery(query, localCache);
		return dhqr;
	}
	private <T extends DataHubModel> ArrayList<T> dhQueryToModel(DHQueryResult dhqr, Class<T> modelClass, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash) throws InstantiationException, IllegalAccessException{
		ArrayList<T> output = new ArrayList<T>();
		if(dhqr == null){
			return output;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = (T) modelClass.newInstance();
			updateNewModel(dhqr, i,newObj,recursionDepthLimit, localCache, objectHash);
			output.add(newObj);
		}
		return output;
	}
	private <T extends DataHubModel> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash){
		updateNewModel(dhqr, rowNumber, objectToUpdate, recursionDepthLimit, localCache, null, false, objectHash);
	}
	private <T extends DataHubModel> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ArrayList<String> fieldsToUpdate, boolean idOnly, ConcurrentHashMap<String,Object> objectHash){
		
		String databaseName = this.getDatabaseName();
		String tableName = objectToUpdate.getTableName();
		String completeTableName = objectToUpdate.getCompleteTableName();
		
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		HashMap<String,DHCell> fieldsToDHCell = new HashMap<String,DHCell>();
		
		//invalid conditions, terminate
		if(table.rows.size() == 0){
			return;
		}
		
		//TODO: ID issues
		DHRow row = table.rows.get(rowNumber);
		List<DHField> fields = schema.getFields();
		for(int j = 0; j < fields.size(); j++){
			DHField f = fields.get(j);
			DHCell v = row.getCells().get(j);
			fieldsToDHCell.put(f.name, v);
		}
		//TODO: ID issues
		//ensure id is set before anything and only set the id if the object has an invalid id
		if(!objectToUpdate.validId()){
			if(fieldsToDHCell.containsKey("id")){
				DHCell cell_id = fieldsToDHCell.get("id");
				Resources.convertAndSetField(objectToUpdate, "id", cell_id.value);
			}else{
				//TODO: throw exception here
			}
		}
		if(!idOnly){
			for(Field f1:objectToUpdate.getClass().getFields()){
				//skip setting the id because it was set above
				if(f1.getName().equals("id")){
					continue;
				}
				//figure out fields to update, if fieldsToUpdate is null then update all fields
				//that are not the id
				if(fieldsToUpdate != null && !fieldsToUpdate.contains(f1.getName())){
					continue;
				}
				if(f1.isAnnotationPresent(Column.class)){
					Column c = f1.getAnnotation(Column.class);
					if(fieldsToDHCell.containsKey(c.name())){
						DHCell cell = fieldsToDHCell.get(c.name());
						Resources.convertAndSetField(objectToUpdate, f1.getName(), cell.value);
					}
				}
				if(f1.isAnnotationPresent(Association.class)){
					Association a = f1.getAnnotation(Association.class);
					//TODO:Fix this
					if(a.loadType() == LoadTypes.Eager){
						switch(a.associationType()){
							case HasOne:
								if(DataHubConverter.isModelSubclass(f1.getType())){
									try{
										DHCell cell = fieldsToDHCell.get(a.foreignKey());
										DataHubModel m = (DataHubModel) f1.getType().newInstance();
										String newCompleteTableName = m.getCompleteTableName();
										String query = "select * from "+newCompleteTableName+" where "+newCompleteTableName+"."+a.foreignKey()+" = "+objectToUpdate.id+" LIMIT 1";
										ArrayList<T> newData;
										if(objectHash!=null && objectHash.containsKey(query)){
											newData = (ArrayList<T>) objectHash.get(query);
										}else{
											newData = (ArrayList<T>) this.query(query, m.getClass(),recursionDepthLimit, localCache, objectHash);
											objectHash.put(query, newData);
										}
										if(newData.size() > 0){
											Resources.setField(objectToUpdate, f1.getName(),newData.get(0));
										}
									}catch(Exception e){
										e.printStackTrace();
									}
								 }
								 break;
							case BelongsTo:
								if(DataHubConverter.isModelSubclass(f1.getType())){
									try{
										DHCell cell = fieldsToDHCell.get(a.foreignKey());
										int modelObjectBelongsToId = (int) DataHubConverter.directConvert(cell.value, Integer.TYPE);
										//TODO: object already in memory so can just re-use it instead of making new query
										DataHubModel m = (DataHubModel) f1.getType().newInstance();
										String newCompleteTableName = m.getCompleteTableName();
										//String query = "select * from "+completeTableName+", "+newCompleteTableName+" where "+tableName+".id = "+objectToUpdate.id;
										String query = "select * from "+newCompleteTableName+" where "+newCompleteTableName+".id = "+modelObjectBelongsToId+" LIMIT 1";
										//System.out.println(query);
										ArrayList<T> newData;
										if(objectHash!=null && objectHash.containsKey(query)){
											newData = (ArrayList<T>) objectHash.get(query);
										}else{
											newData = (ArrayList<T>) this.query(query, m.getClass(),recursionDepthLimit, localCache, objectHash);
											objectHash.put(query, newData);
										}
										if(newData.size() > 0){
											Resources.setField(objectToUpdate, f1.getName(),newData.get(0));
										}
									}catch(Exception e){
										
									}
								}
								break;
							case HasMany:
								if(a.associationType() == AssociationTypes.HasMany){
									Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) f1.getType();
									if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
										//fix this
										//make sure id of this object is set before doing this
										try{
											DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
											d.setCurrentModel(objectToUpdate);
											d.setAssociation(a);
											String query = d.getPopulateQuery();
											if(objectHash!=null && objectHash.containsKey(query)){
												d = (DataHubArrayList) objectHash.get(query);
											}else{
												d.populate(recursionDepthLimit, localCache,objectHash);
												objectHash.put(query, d);
											}
											Resources.setField(objectToUpdate, f1.getName(),d);
										}catch(Exception e){
											e.printStackTrace();
										}
									}
								}
								break;
							case HasAndBelongsToMany:
								if(a.associationType() == AssociationTypes.HasAndBelongsToMany){
									Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) f1.getType();
									if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
										//fix this
										//make sure id of this object is set before doing this
										try{
											DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
											d.setCurrentModel(objectToUpdate);
											d.setAssociation(a);
											String query = d.getPopulateQuery();
											if(objectHash.containsKey(query)){
												d = (DataHubArrayList) objectHash.get(query);
											}else{
												d.populate(recursionDepthLimit, localCache,objectHash);
												objectHash.put(query, d);
											}
											Resources.setField(objectToUpdate, f1.getName(),d);
										}catch(Exception e){
											e.printStackTrace();
										}
									}
								}
								break;
							default:
								break;
						}
					}
				}
			}
			//put stuff here
		}
	}
}
