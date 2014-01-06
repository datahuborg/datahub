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

import Annotations.association;
import Annotations.association.AssociationType;
import Annotations.column;
import Annotations.database;
import Annotations.column.Index;
import DataHubAccount.DataHubAccount;
import DataHubResources.Resources;
import DataHubUpdater.DataHubCache;
import DataHubUpdater.DataHubConsistencySpecifier;

@database(name="")
public abstract class Database {
	//TODO: issue with stale objects on same system, could keep track of stale objects and update all of them
	
	protected static int MAX_LOAD_RECURSION_DEPTH = 3;
	
	//prevent do unnecessary saves
	protected static int MAX_SAVE_RECURSION_DEPTH = 2;
	
	private DataHubClient dhc;
	
	private DataHubCache dhcp;
	
	private DataHubConsistencySpecifier dhcs;
	
	public Database(){
		this.dhcp = new DataHubCache();
		this.dhcs = new DataHubConsistencySpecifier();
	}
	public void setDataHubAccount(DataHubAccount dha){
		this.dhc = new DataHubClient(dha);
	}
	public void setCachingPolicy(DataHubCache dhcp){
		this.dhcp = dhcp;
	}
	public void setConsistencyPolicy(DataHubConsistencySpecifier dhcs){
		this.dhcs = dhcs;
	}
	public void connect() throws DataHubException{
		try {
			dhc.connect(this);
		} catch (Exception e){
			//fix this
			throw new DataHubException("Cannot connect to database!");
		}
		instantiateAndSetup();
	}
	public void disconnect(){
		dhc.disconnect();
	}
	private void instantiateAndSetup(){
		//System.out.println("called");
		ArrayList<Field> fields = DataHubConverter.findModels(this);
		try{
			Model.setDatabase(this);
			DataHubArrayList.setDatabase(this);
		}catch(Exception e){
			e.printStackTrace();
		}
		for(Field f:fields){
			Resources.setField(this,f.getName(), Resources.fieldToInstance(f));
		}
	}
	public String getDatabaseName(){
		database d = this.getClass().getAnnotation(database.class);
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
				//System.out.println(this.cache.keySet());
				//System.out.println(query);
				missCount+=1;
				//System.out.println(query);
				//System.out.println("network");
				DHQueryResult out = dhc.dbQuery(query);
				localCache.put(query, out);
				return out;
			}
		}else{
			return dhc.dbQuery(query);
		}
	}
	protected void query(String query){
		this.dbQuery(query, new ConcurrentHashMap<String,Object>());
	}
	protected <T extends Model> ArrayList<T> query(String query, Class<T> modelClass, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache){
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
			output = dhQueryToModel(this.dbQuery(query, localCache), modelClass,recursionDepthLimit-1, localCache);
		}catch(Exception e){
			e.printStackTrace();
		}
		return output;
	}
	protected <T extends Model> void updateModelObject(T model, int recursionDepthLimit,ConcurrentHashMap<String,Object> localCache){
		//TODO:VERY BIG ISSUE HERE, need to get id somehow, not sure how though
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateSQLRep("AND");
		//System.out.println(query);
		DHQueryResult dhqr = this.dbQuery(query, localCache);
		updateNewModel(dhqr, 0, model, recursionDepthLimit, localCache);
	}
	protected <T extends Model> void updateModelId(T model,int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache){
		String query = "SELECT * FROM "+ model.getCompleteTableName()+" WHERE "+model.generateSQLRep("AND");
		DHQueryResult dhqr = this.dbQuery(query, localCache);
		updateNewModel(dhqr, 0, model,recursionDepthLimit, localCache, true);
	}
	public <T extends Model> ArrayList<T> query(String query, Class<T> modelClass){
		return query(query,modelClass,Database.MAX_LOAD_RECURSION_DEPTH, new ConcurrentHashMap<String,Object> ());
	}
	private <T extends Model> ArrayList<T> dhQueryToModel(DHQueryResult dhqr, Class<T> modelClass, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache) throws InstantiationException, IllegalAccessException{
		ArrayList<T> output = new ArrayList<T>();
		if(dhqr == null){
			return output;
		}
		DHData data = dhqr.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
		for(int i = 0; i < table.rows.size(); i++){
			T newObj = (T) modelClass.newInstance();
			updateNewModel(dhqr, i,newObj,recursionDepthLimit, localCache);
			output.add(newObj);
		}
		return output;
	}
	private <T extends Model> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache){
		updateNewModel(dhqr, rowNumber, objectToUpdate, recursionDepthLimit, localCache, false);
	}
	private <T extends Model> void updateNewModel(DHQueryResult dhqr, int rowNumber, T objectToUpdate, int recursionDepthLimit, ConcurrentHashMap<String,Object> localCache, boolean idOnly){
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
				Resources.setField(objectToUpdate, "id", cell_id.value);
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
				if(f1.isAnnotationPresent(column.class)){
					column c = f1.getAnnotation(column.class);
					if(fieldsToDHCell.containsKey(c.name())){
						DHCell cell = fieldsToDHCell.get(c.name());
						Resources.setField(objectToUpdate, f1.getName(), cell.value);
					}
				}
				if(f1.isAnnotationPresent(association.class)){
					association a = f1.getAnnotation(association.class);
					//TODO:Fix this
					switch(a.associationType()){
						case HasOne:
							if(DataHubConverter.isModelSubclass(f1.getType())){
								try{
									DHCell cell = fieldsToDHCell.get(a.foreignKey());
									Model m = (Model) f1.getType().newInstance();
									String newCompleteTableName = m.getCompleteTableName();
									String query = "select * from "+newCompleteTableName+" where "+newCompleteTableName+"."+a.foreignKey()+" = "+objectToUpdate.id+" LIMIT 1";
									ArrayList<T> newData = (ArrayList<T>) this.query(query, m.getClass(),recursionDepthLimit, localCache);
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
									int modelObjectBelongsToId = (int) Resources.convert(cell.value, Integer.TYPE);
									//TODO: object already in memory so can just re-use it instead of making new query
									Model m = (Model) f1.getType().newInstance();
									String newCompleteTableName = m.getCompleteTableName();
									//String query = "select * from "+completeTableName+", "+newCompleteTableName+" where "+tableName+".id = "+objectToUpdate.id;
									String query = "select * from "+newCompleteTableName+" where "+newCompleteTableName+".id = "+modelObjectBelongsToId+" LIMIT 1";
									//System.out.println(query);
									ArrayList<T> newData = (ArrayList<T>) this.query(query, m.getClass(),recursionDepthLimit, localCache);
									if(newData.size() > 0){
										Resources.setField(objectToUpdate, f1.getName(),newData.get(0));
									}
								}catch(Exception e){
									
								}
							}
							break;
						case HasMany:
							if(a.associationType() == AssociationType.HasMany){
								Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) f1.getType();
								if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
									//fix this
									//make sure id of this object is set before doing this
									try{
										DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
										d.setCurrentModel(objectToUpdate);
										d.setAssociation(a);
										d.populate(recursionDepthLimit, localCache);
										Resources.setField(objectToUpdate, f1.getName(),d);
									}catch(Exception e){
										e.printStackTrace();
									}
								}
							}
							break;
						case HasAndBelongsToMany:
							if(a.associationType() == AssociationType.HasAndBelongsToMany){
								Class<? extends DataHubArrayList> listClass = (Class<? extends DataHubArrayList>) f1.getType();
								if(DataHubConverter.isDataHubArrayListSubclass(listClass)){
									//fix this
									//make sure id of this object is set before doing this
									try{
										DataHubArrayList d = (DataHubArrayList) listClass.newInstance();
										d.setCurrentModel(objectToUpdate);
										d.setAssociation(a);
										d.populate(recursionDepthLimit, localCache);
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
	}
}
