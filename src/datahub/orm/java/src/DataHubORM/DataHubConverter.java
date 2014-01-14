package DataHubORM;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;

import javax.print.DocFlavor.STRING;

import android.R.bool;

import Annotations.Association;
import Annotations.Association.AssociationTypes;
import Annotations.Association.RemovalOptions;
import Annotations.BooleanField;
import Annotations.CharField;
import Annotations.Column;
import Annotations.Column.Index;
import Annotations.DateTimeField;
import Annotations.DoubleField;
import Annotations.IntegerField;
import Annotations.Table;
import Annotations.VarCharField;
import DataHubResources.Constants;
import DataHubResources.Resources;

import datahub.DHType;

public class DataHubConverter {
	public static <T extends DataHubDatabase> String convertDBToSQLSchemaString(Class<T> db) throws DataHubException{
		
		class AssociationModifierHandler{
			public String generateModifierString(Association a){
				String modifierString = "";
				String removalOptions = "";
				switch(a.removalOption()){
					case CascadingDelete:
						removalOptions+="on delete cascade";
						break;
					default:
						break;
				}
				modifierString += removalOptions;
				return modifierString;
			}
		}
		
		ArrayList<Field> models = findModels(db);
		
		HashMap<String,String> tableDefinitions = new HashMap<String,String>();
		
		for(Field f: models){
			DataHubModel currentModel =  null;
			try{
				currentModel = (DataHubModel) f.getType().newInstance();
			}catch(Exception e){
				
			}
			String modelBasic = convertModelBasicTOSQLSchemaString((Class<DataHubModel>)f.getType());
			tableDefinitions.put(currentModel.getCompleteTableName(), modelBasic);
		}
		
		HashMap<String,String>finalTableDefinitions = new HashMap<String,String>();
		HashMap<String,ArrayList<String>>finalTableDefinitionsModifiers = new HashMap<String,ArrayList<String>>();
		
		for(Field f: models){
			
			HashMap<Field,DHType> associations = extractAssociationsFromClass(f.getType()).get(f.getType());
			
			for(Field association: associations.keySet()){	
				
				Association a = association.getAnnotation(Association.class);
				DataHubModel currentModel = null;
				try{
					currentModel = (DataHubModel) f.getType().newInstance();
				}catch(Exception e){
					
				}
				String key;
				switch(a.associationType()){
					case BelongsTo:
						try{
							DataHubModel otherModel = (DataHubModel) association.getType().newInstance();
							key = currentModel.getCompleteTableName();
							//current model belongs to another model specified by association field so
							//current model needs foreign key column
							if(!finalTableDefinitions.containsKey(key)){
								String tableDef = tableDefinitions.get(key);
								//TODO:change this so we use primary key of other table instead of id
								tableDef=tableDef.substring(0, tableDef.length()-1);
								tableDef+=", "+a.foreignKey()+" integer, foreign key ("+a.foreignKey()+") references "+otherModel.getCompleteTableName()+"("+"id"+") ";
								finalTableDefinitions.put(key, tableDef);
							}
						}catch(Exception e){
							throw new DataHubException("Invalid model association! A BelongsTo Annotation can only be used on a DataHubModel field!");
						}
						break;
					case HasOne: 
						try{
							DataHubModel otherModel = (DataHubModel) association.getType().newInstance();
							key = otherModel.getCompleteTableName();
							if(!finalTableDefinitions.containsKey(key)){
								String tableDef = tableDefinitions.get(key);
								tableDef=tableDef.substring(0, tableDef.length()-1);
								//TODO:change this so we use primary key of other table instead of id
								tableDef+=", "+a.foreignKey()+" integer, foreign key ("+a.foreignKey()+") references "+currentModel.getCompleteTableName()+"("+"id"+") ";
								finalTableDefinitions.put(key, tableDef);
							}
						}catch(Exception e){
							throw new DataHubException("Invalid model association for field: "+association.getName()+" in "+f.getName()+"! A HasOne Annotation can only be used on a DataHubModel field!");
						}
						break;
					case HasMany:
						try{
							DataHubArrayList otherModelList = (DataHubArrayList) association.getType().newInstance();
							DataHubModel otherModel = (DataHubModel) otherModelList.getAssociatedModelClass().newInstance();
							key = otherModel.getCompleteTableName();
							if(!finalTableDefinitions.containsKey(key)){
								String tableDef = tableDefinitions.get(key);
								tableDef=tableDef.substring(0, tableDef.length()-1);
								//TODO:change this so we use primary key of other table instead of id
								tableDef+=", "+a.foreignKey()+" integer, foreign key ("+a.foreignKey()+") references "+currentModel.getCompleteTableName()+"("+"id"+") ";
								finalTableDefinitions.put(key, tableDef);
							}
						}catch(Exception e){
							//e.printStackTrace();
							throw new DataHubException("Invalid model association for field: "+association.getName()+" in "+f.getName()+"! A HasMany Annotation can only be used on a DataHubArrayList field!");
						}
						break;
					case HasAndBelongsToMany:
						try{
							DataHubArrayList otherModelList = (DataHubArrayList) association.getType().newInstance();
							String linkingTable = otherModelList.getDatabase().getDatabaseName()+"."+a.linkingTable();
							key = linkingTable;
							if(!finalTableDefinitions.containsKey(key)){
								//add foreign key constraint later
								//foreign key ("+a.foreignKey()+") references "+otherModel.getCompleteTableName()+"("+"id"+") 
								String tableDef = "create table if not exists "+linkingTable+"(id serial,"+a.leftTableForeignKey()+" integer,"+a.rightTableForeignKey()+" integer)";
								finalTableDefinitions.put(key, tableDef);
							}
						}catch(Exception e){
							//e.printStackTrace();
							throw new DataHubException("Invalid model association for field: "+association.getName()+" in "+f.getName()+"! A HasMany Annotation can only be used on a DataHubArrayList field!");
						}
						break;
					default:
						throw new DataHubException("Invalid model association for field: "+association.getName()+" in "+f.getName());
				}
				ArrayList<String> modifiers = new ArrayList<String>();
				if(finalTableDefinitionsModifiers.containsKey(key)){
					modifiers = finalTableDefinitionsModifiers.get(key);
				}
				String newModifier = new AssociationModifierHandler().generateModifierString(a);
				if(!modifiers.contains(newModifier) && !newModifier.equals("")){
					modifiers.add(newModifier);
				}
				finalTableDefinitionsModifiers.put(key, modifiers);
			}
		}
		for(String key:finalTableDefinitions.keySet()){
			String value = finalTableDefinitions.get(key);
			if(finalTableDefinitionsModifiers.containsKey(key)){
				value+=Resources.concatenate(finalTableDefinitionsModifiers.get(key), " ")+")";
				finalTableDefinitions.put(key, value);
			}
		}
		for(String table: tableDefinitions.keySet()){
			if(!finalTableDefinitions.containsKey(table)){
				finalTableDefinitions.put(table, tableDefinitions.get(table));
			}
		}
		//move tables with foreign key constraints after tables without them so
		//no sql errors thrown
		ArrayList<String> before = new ArrayList<String>();
		ArrayList<String> after = new ArrayList<String>();
		for(String value:finalTableDefinitions.values()){
			if(value.contains("foreign key")){
				after.add(value);
			}else{
				before.add(value);
			}
		}
		before.addAll(after);
		return Resources.concatenate(before, ";");
	}
	public static <T extends DataHubModel> String convertModelBasicTOSQLSchemaString(Class<T> c) throws DataHubException{
		HashMap<Class,HashMap<Field,DHType>> basicFields = extractColumnBasicFromClass(c);
		HashMap<Field,DHType> basicColumns = basicFields.get(c);
		DataHubModel m =  null;
		try{
			m = (DataHubModel) c.newInstance();
		}catch(Exception e){
			throw new DataHubException("Could not convert model to SQL. "+e.getMessage());
		}
		String tableSQL = "create table if not exists "+m.getCompleteTableName()+"(";
		
		ArrayList<String> columnNamesAndDataTypes = new ArrayList<String>();
		int primaryKeyCount = 0;
		for(Field f: basicColumns.keySet()){
			Column column = f.getAnnotation(Column.class);
			String columnStr = column.name()+" "+modelTypeToSQLString(f);
			if(column.index() == Index.PrimaryKey){
				columnStr+=" "+"primary key";
				primaryKeyCount++;
			}
			columnNamesAndDataTypes.add(columnStr);
		}
		//validity checks
		if(primaryKeyCount > 1){
			//TODO: support combo primary key
			throw new DataHubException("DataHubModel classes only support one primary key!");
		}
		tableSQL+=Resources.concatenate(columnNamesAndDataTypes,",")+")";
		return tableSQL;
	}
	public static <T extends DataHubDatabase> ArrayList<HashMap<Class,HashMap<Field,DHType>>> convertDBToSchema(Class<T> db){
		ArrayList<HashMap<Class,HashMap<Field,DHType>>> out = new ArrayList<HashMap<Class,HashMap<Field,DHType>>>();
		ArrayList<Field> models = findModels(db);
		for(Field model: models){
			out.add(extractColumnBasicFromClass(model.getType()));
		}
		return out;
	}
	public static <T extends DataHubDatabase> ArrayList<Field> findModels(Class<T> db){
		Field[] dbFields = db.getFields();
		ArrayList<Field> modelFields = new ArrayList<Field>();
		for(Field f:dbFields){
			//get type which is type of object held in field not Field Class
			if(isModelSubclass(f.getType())){
				modelFields.add(f);
			}
		}
		return modelFields;
	}
	public static boolean isModelSubclass(Class c){
		try{
			if(c.equals(DataHubModel.class) || c.asSubclass(DataHubModel.class) != null){
				return true;
			}
		}catch(Exception e){
			//e.printStackTrace();
		}
		return false;
	}
	public static boolean isDataHubArrayListSubclass(Class c){
		try{
			if(c.equals(DataHubArrayList.class) || c.asSubclass(DataHubArrayList.class) != null){
				return true;
			}
		}catch(Exception e){
			//e.printStackTrace();
		}
		return false;
	}
	public static HashMap<Class,HashMap<Field,DHType>> extractColumnBasicFromClass(Class model){
		return extractDataFromClass(model,true);
	}
	public static HashMap<Class,HashMap<Field,DHType>> extractAssociationsFromClass(Class model){
		return extractDataFromClass(model,false);
	}
	public static HashMap<Class,HashMap<Field,DHType>> extractDataFromClass(Class model, boolean basic){
		
		//TODO: do model type checks here
		
		//output hashmaps
		HashMap<Class,HashMap<Field,DHType>> output = new HashMap<Class,HashMap<Field,DHType>>();
		HashMap<Field,DHType> fieldsDHType = new HashMap<Field,DHType>();
		
		//model fields
		Field[] fields = model.getFields();
		
		//table annotation detection
		int tableCount = 0;
		String tableName = null;
		
		//iterate over all fields
		for(Field f:fields){
			//check for column annotation
			if(hasColumnBasic(f)){
				if(basic){
					fieldsDHType.put(f, modelTypeToDHType(f));
					continue;
				}
			}
			if(hasAssociation(f)){
				if(!basic){
					fieldsDHType.put(f, modelTypeToDHType(f));
					continue;
				}
			}
		}
		//check for table annotation
		if(model.isAnnotationPresent(Table.class)){
			try {
				//update table information
				tableName = ((Table) model.getAnnotation(Table.class)).name();
				tableCount++;
				if(tableCount > 1){
					throw new Exception("Too many tables!");
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		//ensure table exists before returning anything
		if(tableName != null){
			output.put(model, fieldsDHType);
		}
		return output;
	}
	public static boolean hasColumnBasic(Field f){
		if(f.isAnnotationPresent(Column.class)){
			return true;
		}
		return false;
	}
	public static boolean hasAssociation(Field f){
		if(f.isAnnotationPresent(Association.class)){
			return true;
		}
		return false;
	}
	public static boolean hasAssociationHABTM(Field f){
		if(f.isAnnotationPresent(Association.class) && f.getAnnotation(Association.class).associationType() == AssociationTypes.HasAndBelongsToMany){
			return true;
		}
		return false;
	}
	public static String modelTypeToSQLString(Field f) throws DataHubException{
		//System.out.println(Arrays.asList(f.getDeclaredAnnotations()));
		if(f.isAnnotationPresent(Column.class)){
			if(f.isAnnotationPresent(CharField.class)){
				CharField cf = f.getAnnotation(CharField.class);
				if(f.getType().equals(String.class)){
					return "char("+cf.size()+")";
				}
			}
			if(f.isAnnotationPresent(VarCharField.class)){
				VarCharField ccf = f.getAnnotation(VarCharField.class);
				if(f.getType().equals(String.class)){
					return "varchar("+ccf.size()+")";
				}
			}
			if(f.isAnnotationPresent(DoubleField.class)){
				if(f.getType().equals(Double.TYPE)){
					return "decimal";
				}
			}
			if(f.isAnnotationPresent(IntegerField.class)){
				IntegerField intf = f.getAnnotation(IntegerField.class);
				if(f.getType().equals(Integer.TYPE)){
					if(intf.Serial()){
						return "serial";
					}
					return "integer";
				}
			}
			if(f.isAnnotationPresent(DateTimeField.class)){
				if(f.getType().equals(Date.class)){
					return "timestamp";
				}
			}
			if(f.isAnnotationPresent(BooleanField.class)){
				if(f.getType().equals(Boolean.TYPE)){
					return "boolean";
				}
			}
		}
		throw new DataHubException("Invalid model field declaration for: "+f.getName()+"!");
	}
	public static DHType modelTypeToDHType(Field f){
		//convert from annotation to DataHub type
		if(f.isAnnotationPresent(Column.class)){
			if(f.isAnnotationPresent(CharField.class)){
				return DHType.Text;
			}
			if(f.isAnnotationPresent(VarCharField.class)){
				return DHType.Text;
			}
			if(f.isAnnotationPresent(DoubleField.class)){
				return DHType.Double;
			}
			if(f.isAnnotationPresent(IntegerField.class)){
				return DHType.Integer;
			}
			if(f.isAnnotationPresent(DateTimeField.class)){
				return DHType.DateTime;
			}
			if(f.isAnnotationPresent(BooleanField.class)){
				return DHType.Boolean;
			}
		}
		return DHType.Binary;
	}
	public static Object convertToJavaType(Object c, Field f) throws DataHubException{
		if(f.isAnnotationPresent(Column.class)){
			if(f.isAnnotationPresent(CharField.class)){
				if(f.getType().equals(String.class)){
					return new String(((ByteBuffer) c).array());
				}
			}
			if(f.isAnnotationPresent(VarCharField.class)){
				if(f.getType().equals(String.class)){
					return new String(((ByteBuffer) c).array());
				}
			}
			if(f.isAnnotationPresent(DoubleField.class)){
				if(f.getType().equals(Double.class)){
					double result = Double.parseDouble(new String(((ByteBuffer) c).array()));
					return result;
				}
				if(f.getType().equals(Float.class)){
					float result = Float.parseFloat(new String(((ByteBuffer) c).array()));
					return result;
				}
			}
			if(f.isAnnotationPresent(IntegerField.class)){
				if(f.getType().equals(Integer.class)){
					int result = Integer.parseInt(new String(((ByteBuffer) c).array()));
					return result;
				}
			}
			if(f.isAnnotationPresent(DateTimeField.class)){
				if(f.getType().equals(Date.class)){
					Date result = new Date(Date.parse(new String(((ByteBuffer) c).array())));
					return result;
				}
			}
			if(f.isAnnotationPresent(BooleanField.class)){
				if(f.getType().equals(Boolean.class)){
					Boolean result = Boolean.parseBoolean(new String(((ByteBuffer) c).array()));
					return result;
				}
			}
		}
		throw new DataHubException("Invalid model field declaration for: "+f.getName()+"!");
	}
	public static Object directConvert(Object c, Type t){
		if(t.equals(Integer.TYPE)){
			int result = Integer.parseInt(new String(((ByteBuffer) c).array()));
			return result;
		}
		if(t.equals(String.class)){
			return new String(((ByteBuffer) c).array());
		}
		return null;
	}
}
