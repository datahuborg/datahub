package DataHubORM;

import java.lang.reflect.Field;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
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

import Configurations.DataHubCache;
import Configurations.DataHubConsistencySpecifier;
import DataHubAccount.DataHubAccount;
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
	
	
	protected static int MAX_LOAD_RECURSION_DEPTH = Integer.MAX_VALUE;
	
	//prevent unnecessary saves
	protected static int MAX_SAVE_RECURSION_DEPTH = Integer.MAX_VALUE;
	
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
	DHQueryResult dbQuery(String query){
		return dhc.dbQuery(query);
	}
	private DHQueryResult dbQuery(String query, ConcurrentHashMap<String,Object> localCache){
		//System.out.println(query);
		//System.out.println(dhc.dbQuery(query));
		if(query.toLowerCase().startsWith("select * from") || query.toLowerCase().startsWith("(select * from")){
			if(localCache.containsKey(query)){
				//System.out.println(query);
				hitCount+=1;
				return (DHQueryResult) localCache.get(query);
			}else{
				//System.out.println(localCache.keySet());
				System.out.println(query);
				missCount+=1;
				//System.out.println(query);
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
		try{
			output = dhQueryToModel(this.dbQuery(query, localCache), modelClass,recursionDepthLimit-1, localCache, objectHash);
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	<T extends DataHubModel> void updateModelObject(T model, int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache,ConcurrentHashMap<String,Object> objectHash){
		updateModel(getModelBasicDHQuerResult(model, localCache),model, recursionDepthLimit, localCache,objectHash);
	}
	<T extends DataHubModel> void updateModelId(T model){
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
		if(dhqr == null || recursionDepthLimit == 0){
			return output;
		}
		DHData data = dhqr.getData();
		DHTable table  = data.getTable();
		
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = (T) modelClass.newInstance();
			//update model basic fields
			output.add(newObj);
		}
		updateNewModels(dhqr, output,recursionDepthLimit,localCache,objectHash);
		return output;
	}
	private <T extends DataHubModel> void updateModel(DHQueryResult dhqr, T objectToUpdate, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash){
		updateModel(dhqr, objectToUpdate, recursionDepthLimit, localCache, null, false, objectHash);
	}
	private <T extends DataHubModel> void updateModel(DHQueryResult dhqr, T objectToUpdate,  int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ArrayList<String> fieldsToUpdate, boolean idOnly, ConcurrentHashMap<String,Object> objectHash){
		ArrayList<T> models = new ArrayList<T>();
		models.add(objectToUpdate);
		updateNewModels(dhqr, models, recursionDepthLimit, localCache, fieldsToUpdate, idOnly, objectHash);
	}
	private <T extends DataHubModel> void updateNewModels(DHQueryResult dhqr, ArrayList<T> models, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ConcurrentHashMap<String,Object> objectHash){
		updateNewModels(dhqr, models, recursionDepthLimit, localCache, null, false, objectHash);
	}
	
	private <T extends DataHubModel> void updateNewModels(DHQueryResult dhqr, ArrayList<T> models,  int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, ArrayList<String> fieldsToUpdate, boolean idOnly, ConcurrentHashMap<String,Object> objectHash){
		//System.out.println(recursionDepthLimit);
		if(recursionDepthLimit <= 0){
			return;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		
		ArrayList<LinkedHashMap<Field,String>> queries = new ArrayList<LinkedHashMap<Field,String>>();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = models.get(i);
			queries.add((LinkedHashMap<Field, String>) setBasicAndGetRelatedQueries(dhqr, i,newObj,fieldsToUpdate,idOnly));
		}
		if(idOnly){
			return;
		}
		//System.out.println(queries);
		LinkedHashMap<Field,String> queries1 = new LinkedHashMap<Field,String>();
		LinkedHashMap<Field,ArrayList<String>> queryOrders = new LinkedHashMap<Field,ArrayList<String>>();
		for(HashMap<Field,String> data1: queries){
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
		for(Field field1: queries1.keySet()){
			ArrayList<String> queryOrdersForCurrentField = queryOrders.get(field1);
			String actualQuery = queries1.get(field1);
			
			//actual network request made here
			DHQueryResult dhqr1 = this.dbQuery(actualQuery, localCache);
			
			
			ArrayList<DHQueryResult> queryResults = new ArrayList<DHQueryResult>();
			List<DHField> fields = dhqr1.data.schema.getFields();
			LinkedHashMap<String,Integer> fieldsToIndex = new LinkedHashMap<String,Integer>();
			for(int j = 0; j < fields.size(); j++){
				DHField f = fields.get(j);
				fieldsToIndex.put(f.name, j);
			}
			int lastDivision = 0;
			int idIndex = fieldsToIndex.get("id");
			for(int i = 0; i < dhqr1.data.table.rows.size(); i++){
				DHRow dhrow = dhqr1.data.table.rows.get(i);
				if(DataHubConverter.convertToString(dhrow.getCells().get(idIndex).value).equals("None") && i<(dhqr1.data.table.rows.size()-1)){
					DHQueryResult newDhqr = dhqr1.deepCopy();
					if(lastDivision!=i && lastDivision<=i){
						newDhqr.data.table.rows = newDhqr.data.table.rows.subList(lastDivision, i);
					}else{
						newDhqr.data.table.rows.clear();
					}
					lastDivision = i+1;
					queryResults.add(newDhqr);
				}
			}
			if(lastDivision<dhqr1.data.table.rows.size()){
				DHQueryResult newDhqr = dhqr1.deepCopy();
				newDhqr.data.table.rows = newDhqr.data.table.rows.subList(lastDivision, dhqr1.data.table.rows.size()-1);
				queryResults.add(newDhqr);
			}
			int end = Math.min(queryResults.size(), queries.size());
			//System.out.println(queryResults);
			for(int k = 0; k < end; k++){
				T data1  = models.get(k);
				DHQueryResult corresponingResults  = queryResults.get(k);
				String currentQuery = queryOrdersForCurrentField.get(k);
				
				localCache.put(currentQuery, corresponingResults);
				
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
										ArrayList<DataHubModel> results = new ArrayList<DataHubModel>();
										if(objectHash.containsKey(currentQuery)){
											//System.out.println("found"+currentQuery);
											results = (ArrayList<DataHubModel>) objectHash.get(currentQuery);
										}else{
											objectHash.put(currentQuery, results);
											results.addAll((ArrayList<DataHubModel>)dhQueryToModel(corresponingResults,(Class<? extends DataHubModel>)field1.getType(),recursionDepthLimit-1,localCache,objectHash));
										}
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
										ArrayList<DataHubModel> results = new ArrayList<DataHubModel>();
										if(objectHash.containsKey(currentQuery)){
											//System.out.println("found"+currentQuery);
											results = (ArrayList<DataHubModel>) objectHash.get(currentQuery);
										}else{
											objectHash.put(currentQuery, results);
											results.addAll((ArrayList<DataHubModel>)dhQueryToModel(corresponingResults,(Class<? extends DataHubModel>)field1.getType(),recursionDepthLimit-1,localCache,objectHash));
										}
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
											ArrayList<DataHubModel> results = new ArrayList<DataHubModel>();
											if(objectHash.containsKey(currentQuery)){
												//System.out.println("found"+currentQuery);
												results = (ArrayList<DataHubModel>) objectHash.get(currentQuery);
											}else{
												objectHash.put(currentQuery, results);
												results.addAll(dhQueryToModel(corresponingResults,(Class<? extends DataHubModel>)d.getAssociatedModelClass(),recursionDepthLimit-1,localCache,objectHash));
											}
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
											ArrayList<DataHubModel> results = new ArrayList<DataHubModel>();
											if(objectHash.containsKey(currentQuery)){
												//System.out.println("found"+currentQuery);
												results = (ArrayList<DataHubModel>) objectHash.get(currentQuery);
											}else{
												objectHash.put(currentQuery, results);
												results.addAll(dhQueryToModel(corresponingResults,(Class<? extends DataHubModel>)d.getAssociatedModelClass(),recursionDepthLimit-1,localCache,objectHash));
											}
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
	private <T extends DataHubModel> LinkedHashMap<Field,String> setBasicAndGetRelatedQueries(DHQueryResult dhqr, int rowNumber, T objectToUpdate, ArrayList<String> fieldsToUpdate, boolean idOnly){
		
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
								try{
									DataHubModel currentModel = (DataHubModel) f1.getDeclaringClass().newInstance();
									DataHubModel otherModel = (DataHubModel) f1.getType().newInstance();
									String foreignKey = DataHubConverter.AssociationDefaultsHandler.getForeignKey(a, currentModel, otherModel);
									
									DHCell cell = fieldsToDHCell.get(foreignKey);
									int modelObjectBelongsToId = (int) DataHubConverter.directConvert(cell.value, Integer.TYPE);
									
									
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
