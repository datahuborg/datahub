package DataHubORM;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.apache.thrift.TException;


import datahub.DHCell;
import datahub.DHData;
import datahub.DHException;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;

import Configurations.DataHubCache;
import Configurations.DataHubConsistencySpecifier;
import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubAnnotations.Association;
import DataHubAnnotations.Column;
import DataHubAnnotations.Database;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Association.LoadTypes;
import DataHubAnnotations.Column.Index;
import DataHubResources.Resources;
import DataHubWorkers.DataHubWorker;
import DataHubWorkers.GenericCallback;
import DataHubWorkers.GenericExecutable;
import DataHubWorkers.DataHubWorker.DataHubWorkerMode;

@Database(name="")
public class DataHubDatabase {
	//TODO: issue with stale objects on same system, could keep track of stale objects and update all of them
	
	public enum DatabaseEngine{Postgres};
	
	
	protected static int MAX_LOAD_RECURSION_DEPTH = 3;
	
	//prevent unnecessary saves
	protected static int MAX_SAVE_RECURSION_DEPTH = 5;
	
	protected static int MAX_THREADS =1;
	
	private DataHubClient dhc;
	
	private DataHubAccount dha;
	
	private DatabaseEngine databaseEngine;
	
	private DataHubWorkerMode dataHubWorkerMode;
	
	DataHubModel sentinel = null;
	
	public DataHubDatabase() throws DataHubException{
		this(true);
	}
	public DataHubDatabase(boolean setup) throws DataHubException{
		this.dataHubWorkerMode = DataHubWorkerMode.Normal;
		if(setup){
			this.instantiateAndSetup();
		}
	}
	public synchronized void setDataHubAccount(DataHubAccount dha){
		this.dha = dha;
		this.dhc = new DataHubClient(dha);
		this.dhc.setDatabase(this);
	}
	public synchronized void setDataHubWorkerMode(DataHubWorkerMode dataHubWorkerMode){
		this.dataHubWorkerMode = dataHubWorkerMode;
	}
	public synchronized DataHubWorkerMode getDataHubWorkerMode(){
		return dataHubWorkerMode;
	}
	DataHubDatabase copy() throws DataHubException{
		DataHubDatabase newDB = new DataHubDatabase(false);
		newDB.dataHubWorkerMode = this.dataHubWorkerMode;
		newDB.databaseEngine = this.databaseEngine;
		newDB.setDataHubAccount(new DataHubAccount(dha.getApiKey(), new DataHubUser(dha.getUser().getUsername(), dha.getUser().getPassword())));
		return newDB;
	}
	public synchronized void clearAndReCreate() throws DataHubException{
		//clear database
		String clearDB = "drop schema if exists "+this.getDatabaseName()+" cascade;";
		
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
	private void instantiateAndSetup() throws DataHubException{
		ArrayList<Field> fields = DataHubConverter.findModels(this.getClass());
		for(Field f:fields){
			Class c = f.getType();
			if(DataHubConverter.isModelSubclass(c)){
				DataHubModel.setDatabase(c, this);
			}
			Resources.setField(this,f.getName(), Resources.fieldToInstance(f));
		}
		//sentinel = new DataHubModel(){};
	}
	public synchronized String getDatabaseName(){
		try {
			return DataHubConverter.getDatabaseName(this.getClass());
		} catch (DataHubException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
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
	/*TO BE REMOVED*/
	DHQueryResult dbQuery(String query) throws DataHubException{
		return dhc.dbQuery(query);
	}
	private DHQueryResult dbQuery(String query, ConcurrentHashMap<String,Object> localCache) throws DataHubException{
		//System.out.println(dhc.dbQuery(query));
		if(query.equals("") || query.equals(" ") || query.equals(null)){
			return null;
		}
		if(query.toLowerCase().startsWith("select * from") || query.toLowerCase().startsWith("(select * from")){
			if(localCache.containsKey(query)){
				//System.out.println(query);
				hitCount+=1;
				return (DHQueryResult) localCache.get(query);
			}else{
				//System.out.println(localCache.keySet());
				System.out.println("Miss: "+query);
				missCount+=1;
				//System.out.println(query);
				//System.out.println("network");
//				/System.out.println(Thread.currentThread().getId()+query);
				DHQueryResult out = dhc.dbQuery(query);
				localCache.put(query, out);
				return out;
			}
		}else{
			System.out.println("Mutate: "+query);
			otherCount+=1;
			return dhc.dbQuery(query);
		}
		//return dhc.dbQuery(query);
	}
	void query(String query) throws DataHubException{
		if(!query.equals("") && query!=null){
			this.dbQuery(query, new ConcurrentHashMap<String,Object>());
		}
	}
	<T extends DataHubModel> ArrayList<T> query(String query, Class<T> modelClass, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash){
		ArrayList<T> output = new ArrayList<T>();
		if(recursionDepthLimit <= 0){
			return output;
		}
		try{
			output = dhQueryToModel(this.dbQuery(query, localCache), modelClass,recursionDepthLimit-1, localCache, objectHash);
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	<T extends DataHubModel> void updateModelObject(T model, int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache,ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		updateModel(getModelBasicDHQuerResult(model, localCache),model, recursionDepthLimit, localCache,objectHash);
	}
	<T extends DataHubModel> void updateModelId(T model) throws DataHubException{
		updateModel(getModelBasicDHQuerResult(model),model,1, null, null, true, null);
	}
	<T extends DataHubModel> void updateModelObjectField(String fieldName, T model, int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		if(Resources.hasField(model.getClass(), fieldName)){
			ArrayList<String> fields = new ArrayList<String>();
			fields.add(fieldName);
			updateModel(getModelBasicDHQuerResult(model, localCache),model,recursionDepthLimit, localCache, fields, false, objectHash);
		}else{
			throw new DataHubException("Model: "+this.getClass().getCanonicalName()+" has no field: "+fieldName+". Cannot refresh field!");
		}
	}
	public <T extends DataHubModel> ArrayList<T> query(String query, Class<T> modelClass){
		return query(query,modelClass,DataHubDatabase.MAX_LOAD_RECURSION_DEPTH, new ConcurrentHashMap<String,Object> (),new ConcurrentHashMap<String,Object> ());
	}
	private <T extends DataHubModel> DHQueryResult getModelBasicDHQuerResult(T model) throws DataHubException{
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateQuerySQLRep();
		//System.out.println(query);
		DHQueryResult dhqr = this.dbQuery(query);
		return dhqr;
	}
	private <T extends DataHubModel> DHQueryResult getModelBasicDHQuerResult(T model, ConcurrentHashMap<String,Object> localCache) throws DataHubException{
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateQuerySQLRep();
		//System.out.println(query);
		DHQueryResult dhqr = this.dbQuery(query, localCache);
		return dhqr;
	}
	private <T extends DataHubModel> ArrayList<T> dhQueryToModel(DHQueryResult dhqr, Class<T> modelClass, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash) throws InstantiationException, IllegalAccessException, DataHubException{
		ArrayList<T> output = new ArrayList<T>();
		if(dhqr == null || recursionDepthLimit <= 0){
			return output;
		}
		DHData data = dhqr.getData();
		DHTable table  = data.getTable();
		HashMap<String,Integer> fieldToIndex = new HashMap<String,Integer>();
		
		List<DHField> fields = dhqr.data.schema.getFields();
		LinkedHashMap<String,Integer> fieldsToIndex = new LinkedHashMap<String,Integer>();
		for(int j = 0; j < fields.size(); j++){
			DHField f = fields.get(j);
			fieldsToIndex.put(f.name, j);
		}
		
		for(int i = 0; i < table.rows.size(); i++){
			Object c = dhqr.data.table.rows.get(i).getCells().get(fieldsToIndex.get("id")).value;
			String key = new String(((ByteBuffer) c).array());
			if(key.equals("None")){
				output.add((T) sentinel);
				continue;
			}
			T newObj = (T) modelClass.newInstance();
			//update model basic fields
			output.add(newObj);
		}
		updateNewModels(dhqr, output,recursionDepthLimit,localCache,objectHash);
		return output;
	}
	private <T extends DataHubModel> void updateModel(DHQueryResult dhqr, T objectToUpdate, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		updateModel(dhqr, objectToUpdate, recursionDepthLimit, localCache, null, false, objectHash);
	}
	private <T extends DataHubModel> void updateModel(DHQueryResult dhqr, T objectToUpdate,  int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ArrayList<String> fieldsToUpdate, boolean idOnly, ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		ArrayList<T> models = new ArrayList<T>();
		models.add(objectToUpdate);
		updateNewModels(dhqr, models, recursionDepthLimit, localCache, fieldsToUpdate, idOnly, objectHash);
	}
	private <T extends DataHubModel> void updateNewModels(DHQueryResult dhqr, ArrayList<T> models, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		updateNewModels(dhqr, models, recursionDepthLimit, localCache, null, false, objectHash);
	}
	
	private <T extends DataHubModel> void updateNewModels(DHQueryResult dhqr, ArrayList<T> models,  int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ArrayList<String> fieldsToUpdate, boolean idOnly, ConcurrentHashMap<String,Object> objectHash) throws DataHubException{
		//System.out.println(recursionDepthLimit);
		if(recursionDepthLimit <= 0 || dhqr==null){
			return;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable().deepCopy();
		
		ArrayList<LinkedHashMap<Field,String>> queries = new ArrayList<LinkedHashMap<Field,String>>();
		for(int i = 0; i < models.size(); i++){
			T newObj = models.get(i);
			if(newObj==sentinel){
				continue;
			}
			queries.add((LinkedHashMap<Field, String>) setBasicAndGetRelatedQueries(dhqr, i,newObj,fieldsToUpdate,idOnly));
		}
		if(idOnly){
			return;
		}
		//System.out.println(queries);
		LinkedHashMap<Field,String> queries1 = new LinkedHashMap<Field,String>();
		LinkedHashMap<Field,ArrayList<String>> queryOrders = new LinkedHashMap<Field,ArrayList<String>>();
		for(HashMap<Field,String> data1: queries){
			if(data1==null){
				continue;
			}
			for(Field field: data1.keySet()){
				ArrayList<String> queryOrdersForField;
				if(!queryOrders.containsKey(field)){
					queryOrdersForField = new ArrayList<String>();
				}else{
					queryOrdersForField = queryOrders.get(field);
				}
				DataHubModel newTemplate;
				try{
					if(DataHubConverter.isDataHubArrayListSubclass(field.getType())){
						newTemplate = (DataHubModel) ((DataHubArrayList) field.getType().newInstance()).getAssociatedModelClass().newInstance();
					}else{
						newTemplate = (DataHubModel) field.getType().newInstance();
					}
				}catch(Exception e){
					e.printStackTrace();
					//TODO: fix this error message
					 continue;
				}
				
				queryOrdersForField.add(data1.get(field));
				
				String newQuery = "("+data1.get(field) +") union all ("+ newTemplate.generateNullSelect()+")";
				if(!queries1.containsKey(field)){
					queries1.put(field, newQuery);
				}else{
					queries1.put(field, queries1.get(field)+" union all ("+newQuery+")");
				}
				
				queryOrders.put(field, queryOrdersForField);
			}
		}
		class LoadHelper  implements Runnable{
			volatile ConcurrentHashMap<String,Object> localCache;
			String actualQuery;
			Field f;
			ConcurrentHashMap<Field,DHQueryResult> results;
			public LoadHelper(Field f,ConcurrentHashMap<Field,DHQueryResult> results,String actualQuery,ConcurrentHashMap<String,Object> localCache){
				this.f = f;
				this.results = results;
				this.actualQuery = actualQuery;
				this.localCache = localCache;
			}
			@Override
			public void run() {
				// TODO Auto-generated method stub
				try {
					this.results.put(f, dbQuery(actualQuery, localCache));
				} catch (DataHubException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				try {
					Thread.sleep(10);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			
		}
		ConcurrentHashMap<Field,DHQueryResult> results12 = new ConcurrentHashMap<Field,DHQueryResult>();
		//ArrayList<Thread> threads = new ArrayList<Thread>();
		ExecutorService executor = Executors.newFixedThreadPool(DataHubDatabase.MAX_THREADS);
		for(Field field1: queries1.keySet()){
			String actualQuery = queries1.get(field1);
			executor.execute(new LoadHelper(field1,results12,actualQuery,localCache));
			//Thread t = new Thread(new LoadHelper(field1,results12,actualQuery,localCache));
			//threads.add(t);
		}
		executor.shutdown();
		try {
			executor.awaitTermination(Integer.MAX_VALUE, TimeUnit.SECONDS);
		} catch (InterruptedException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		for(Field field1: queries1.keySet()){
			if(!field1.isAnnotationPresent(Association.class)){
				continue;
			}
			ArrayList<String> queryOrdersForCurrentField = queryOrders.get(field1);
			
			//actual network request made here
			DHQueryResult dhqr1 = results12.get(field1);
			
			
			List<DHField> fields = dhqr1.data.schema.getFields();
			LinkedHashMap<String,Integer> fieldsToIndex = new LinkedHashMap<String,Integer>();
			for(int j = 0; j < fields.size(); j++){
				DHField f = fields.get(j);
				fieldsToIndex.put(f.name, j);
			}
			
			//top level recursion
			String qTOP=Resources.concatenate(queryOrdersForCurrentField, ";");
			ArrayList<DataHubModel> output = new ArrayList<DataHubModel>();
			if(objectHash.contains(qTOP)){
				output=(ArrayList<DataHubModel>) objectHash.get(qTOP);
			}else{
				objectHash.put(qTOP, output);
				try {
					Class<? extends DataHubModel> classToUse = (Class<? extends DataHubModel>)field1.getType();
					if(DataHubConverter.isDataHubArrayListSubclass(field1.getType())){
						Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) field1.getType();
						DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
						classToUse=(Class<? extends DataHubModel>)d.getAssociatedModelClass();
					}
					output.addAll((ArrayList<DataHubModel>)dhQueryToModel(dhqr1,classToUse,recursionDepthLimit-1,localCache,objectHash));
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			ArrayList<ArrayList<DataHubModel>> finalData = new ArrayList<ArrayList<DataHubModel>>();
			ArrayList<DataHubModel> newData = new ArrayList<DataHubModel>();
			
			boolean lastNull = false ;
			for(int i=0; i<output.size(); i++){
				DataHubModel o = output.get(i);
				if(o==null){
					if(i!=0 && !lastNull){
						finalData.add(newData);
						newData = new ArrayList<DataHubModel>();
					}
					lastNull = true;
					continue;
				}
				lastNull = false;
				newData.add(o);
			}
			ArrayList<T> models1 = new ArrayList<T>();
			for(T d:models){
				if(d!=sentinel){
					models1.add(d);
				}
			}
			int end = finalData.size();
			
			for(int k = 0; k < end; k++){
				T data1  = models1.get(k);
				ArrayList<DataHubModel> modelData = finalData.get(k);
						
				//System.out.println(corresponingResults);
				if(field1.isAnnotationPresent(Association.class)){
					Association a = field1.getAnnotation(Association.class);
					//TODO:Fix this
					//System.out.println(a.associationType());
					if(a.loadType() == LoadTypes.Eager){
						switch(a.associationType()){
							case HasOne:
								if(DataHubConverter.isModelSubclass(field1.getType())){
									try{
										ArrayList<DataHubModel> results = modelData;
										if(results.size() > 0){
											Resources.setField(data1, field1.getName(),results.get(0));
										}
									}catch(Exception e){
										e.printStackTrace();
									}
								 }
								 break;
							case BelongsTo:
								if(DataHubConverter.isModelSubclass(field1.getType())){
									try{
										ArrayList<DataHubModel> results = modelData;
										if(results.size() > 0){
											Resources.setField(data1, field1.getName(),results.get(0));
										}
									}catch(Exception e){
										
									}
								}
								break;
							case HasMany:
								if(a.associationType() == AssociationTypes.HasMany){
									Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) field1.getType();
									if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
										//fix this
										//make sure id of this object is set before doing this
										try{
											DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
											ArrayList<DataHubModel> results = modelData;
											d.setCurrentModel(data1);
											d.setAssociation(a);
											d.addAllBasic(results);
											Resources.setField(data1, field1.getName(),d);
										}catch(Exception e){
											e.printStackTrace();
										}
									}
								}
								break;
							case HasAndBelongsToMany:
								if(a.associationType() == AssociationTypes.HasAndBelongsToMany){
									Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) field1.getType();
									if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
										//fix this
										//make sure id of this object is set before doing this
										try{
											DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
											ArrayList<DataHubModel> results = modelData;

											d.setCurrentModel(data1);
											d.setAssociation(a);
											d.addAllBasic(results);
											Resources.setField(data1, field1.getName(),d);
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
		}
	}
	private <T extends DataHubModel> void setBasic(DHQueryResult dhqr, int rowNumber, T objectToUpdate, ArrayList<String> fieldsToUpdate, boolean idOnly){
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
				if(fieldsToUpdate != null && !fieldsToUpdate.contains(f1.getName())){
					continue;
				}
				if(f1.isAnnotationPresent(Column.class)){
					//TODO: fix this
					try {
						String columnName;
						columnName = DataHubConverter.getFieldColumnName(f1);
						if(fieldsToDHCell.containsKey(columnName)){
							DHCell cell = fieldsToDHCell.get(columnName);
							Resources.convertAndSetField(objectToUpdate, f1.getName(), cell.value);
						}
					} catch (DataHubException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
			}
		}
	}
	private <T extends DataHubModel> LinkedHashMap<Field,String> setBasicAndGetRelatedQueries(DHQueryResult dhqr, int rowNumber, T objectToUpdate, ArrayList<String> fieldsToUpdate, boolean idOnly) throws DataHubException{
		
		setBasic(dhqr,rowNumber, objectToUpdate,fieldsToUpdate,idOnly);
		
		
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		HashMap<String,DHCell> fieldsToDHCell = new HashMap<String,DHCell>();
		
		//invalid conditions, terminate
		if(idOnly || table.rows.size() == 0){
			return new LinkedHashMap<Field, String>();
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
		LinkedHashMap<Field, String> data1 = new LinkedHashMap<Field,String>();
		for(Field f1:objectToUpdate.getClass().getFields()){
			//skip setting the id because it was set above
			//figure out fields to update, if fieldsToUpdate is null then update all fields
			//that are not the id
			if(fieldsToUpdate != null && !fieldsToUpdate.contains(f1.getName())){
				continue;
			}
			if(f1.isAnnotationPresent(Association.class)){
				Association a = f1.getAnnotation(Association.class);
				//TODO:Fix this
				if(a.loadType() == LoadTypes.Eager){
					switch(a.associationType()){
						case HasOne:
							if(DataHubConverter.isModelSubclass(f1.getType())){
								if(objectToUpdate.id==0){
									throw new DataHubException("Invalid Id");
								}
								try{
									DataHubModel currentModel = (DataHubModel) f1.getDeclaringClass().newInstance();
									DataHubModel otherModel = (DataHubModel) f1.getType().newInstance();
									String foreignKey = DataHubConverter.AssociationDefaultsHandler.getForeignKey(a, currentModel, otherModel);
									
									
									DHCell cell = fieldsToDHCell.get(foreignKey);
									String otherModelCompleteTableName = otherModel.getCompleteTableName();
									String query = "select * from "+otherModelCompleteTableName+" where "+otherModelCompleteTableName+"."+foreignKey+" = "+objectToUpdate.id;
									data1.put(f1, query);
								}catch(Exception e){
									e.printStackTrace();
								}
							 }
							 break;
						case BelongsTo:
							if(DataHubConverter.isModelSubclass(f1.getType())){
								if(objectToUpdate.id==0){
									throw new DataHubException("Invalid Id");
								}
								try{
									DataHubModel currentModel = (DataHubModel) f1.getDeclaringClass().newInstance();
									DataHubModel otherModel = (DataHubModel) f1.getType().newInstance();
									String foreignKey = DataHubConverter.AssociationDefaultsHandler.getForeignKey(a, currentModel, otherModel);
									
									DHCell cell = fieldsToDHCell.get(foreignKey);
									int modelObjectBelongsToId = (Integer)DataHubConverter.directConvert(cell.value, Integer.TYPE);
									
									
									//handles case where object is initialized and it belongs to another object that has currently
									//not been set (meaning the column that contains the id of the associated object is None and 
									//so has a default id of 0)
									if(modelObjectBelongsToId == 0){
										continue;
									}
									
									//TODO: object already in memory so can just re-use it instead of making new query
									String otherModelCompleteTableName = otherModel.getCompleteTableName();
									//String query = "select * from "+completeTableName+", "+newCompleteTableName+" where "+tableName+".id = "+objectToUpdate.id;
									String query = "select * from "+otherModelCompleteTableName+" where "+otherModelCompleteTableName+".id = "+modelObjectBelongsToId;
									//System.out.println(query);
									data1.put(f1, query);
								}catch(Exception e){
									e.printStackTrace();
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
										data1.put(f1, query);
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
										data1.put(f1, query);
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
		return data1;
	}
}
