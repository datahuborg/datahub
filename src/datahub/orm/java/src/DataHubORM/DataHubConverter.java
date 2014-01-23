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

import DataHubAnnotations.Association;
import DataHubAnnotations.BooleanField;
import DataHubAnnotations.CharField;
import DataHubAnnotations.Column;
import DataHubAnnotations.DateTimeField;
import DataHubAnnotations.DoubleField;
import DataHubAnnotations.IntegerField;
import DataHubAnnotations.Table;
import DataHubAnnotations.VarCharField;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Association.RemovalOptions;
import DataHubAnnotations.Column.Index;
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
								//String tableDef = tableDefinitions.get(key);
								//TODO:change this so we use primary key of other table instead of id
								//tableDef=tableDef.substring(0, tableDef.length()-1);
								String tableDef1="alter table "+key+" add "+a.foreignKey()+" integer";
								String tableDef2 = "alter table "+key+" add foreign key ("+a.foreignKey()+") references "+otherModel.getCompleteTableName()+"("+"id"+") ";
								String tableDef = tableDef1 + ";" + tableDef2;
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
								//String tableDef = tableDefinitions.get(key);
								//tableDef=tableDef.substring(0, tableDef.length()-1);
								//TODO:change this so we use primary key of other table instead of id
								String tableDef1="alter table "+key+" add "+a.foreignKey()+" integer";
								String tableDef2 ="alter table "+key+" add foreign key ("+a.foreignKey()+") references "+currentModel.getCompleteTableName()+"("+"id"+") ";
								String tableDef = tableDef1 + ";" + tableDef2;
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
								//String tableDef = tableDefinitions.get(key);
								//tableDef=tableDef.substring(0, tableDef.length()-1);
								//TODO:change this so we use primary key of other table instead of id
								String tableDef1="alter table "+key+" add "+a.foreignKey()+" integer";
								String tableDef2 = "alter table "+key+" add foreign key ("+a.foreignKey()+") references "+currentModel.getCompleteTableName()+"("+"id"+") ";
								String tableDef = tableDef1 + ";" + tableDef2;
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
							DataHubModel otherModel = (DataHubModel) otherModelList.getAssociatedModelClass().newInstance();
							String linkingTable = otherModelList.getDatabase().getDatabaseName()+"."+a.linkingTable();
							key = linkingTable;
							if(!finalTableDefinitions.containsKey(key)){
								//add foreign key constraint later
								//foreign key ("+a.foreignKey()+") references "+otherModel.getCompleteTableName()+"("+"id"+") 
								String tableDef = "create table if not exists "+linkingTable+"(id serial,";
								String leftTable;
								String rightTable;
								if(a.leftTableForeignKey().equals(a.foreignKey())){
									leftTable = currentModel.getCompleteTableName();
									rightTable = otherModel.getCompleteTableName();
								}else if(a.rightTableForeignKey().equals(a.foreignKey())){
									leftTable = otherModel.getCompleteTableName();
									rightTable = currentModel.getCompleteTableName();
								}else{
									throw new DataHubException("For HABTM association, the foreign key must match either the left or the right key in the linking table!");
								}
								String left = a.leftTableForeignKey()+" integer, foreign key ("+a.leftTableForeignKey()+") references "+leftTable+"("+"id"+") " + new AssociationModifierHandler().generateModifierString(a); 
								String right = a.rightTableForeignKey()+" integer, foreign key ("+a.rightTableForeignKey()+") references "+rightTable+"("+"id"+") " + new AssociationModifierHandler().generateModifierString(a); 
								tableDef+= left+","+right+")";
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
				if(a.associationType() != AssociationTypes.HasAndBelongsToMany){
					if(finalTableDefinitionsModifiers.containsKey(key)){
						modifiers = finalTableDefinitionsModifiers.get(key);
					}
					String newModifier = new AssociationModifierHandler().generateModifierString(a);
					if(!modifiers.contains(newModifier) && !newModifier.equals("")){
						modifiers.add(newModifier);
					}
				}
				finalTableDefinitionsModifiers.put(key, modifiers);
			}
		}
		//TODO: fix modifier generation, this code is bad if more than one foreign key
		for(String key:finalTableDefinitions.keySet()){
			String value = finalTableDefinitions.get(key);
			if(finalTableDefinitionsModifiers.containsKey(key) && finalTableDefinitionsModifiers.get(key).size() > 0){
				value+=Resources.concatenate(finalTableDefinitionsModifiers.get(key), " ");
				finalTableDefinitions.put(key, value);
			}
		}
		//move tables with foreign key constraints after tables without them so
		//no sql errors thrown
		//System.out.println(Resources.concatenate(before, ";"));
		String out = Resources.concatenate(tableDefinitions.values(), ";")+";"+Resources.concatenate(finalTableDefinitions.values(), ";");
		return out;
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
			switch(column.index()){
				case PrimaryKey:
					columnStr+=" "+"primary key";
					primaryKeyCount++;
					break;
				default:
					break;
			}
			switch(column.notNullConstraint()){
				case NotNull:
					columnStr+=" "+"not null";
					break;
				default:
					break;
			}
			switch(column.uniquenessConstraint()){
				case Unique:
					columnStr+=" "+"unique";
					break;
				default:
					break;
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
		String modifier = "";
		try{
			DataHubModel modelObject = (DataHubModel) f.getDeclaringClass().newInstance();
			Object val = f.get(modelObject);
			if(val!=null){
				modifier+=" default "+Resources.objectToSQL(val);
			}
		}catch(Exception  e){
			
		}
		if(f.isAnnotationPresent(Column.class)){
			if(f.isAnnotationPresent(CharField.class)){
				CharField cf = f.getAnnotation(CharField.class);
				if(f.getType().equals(String.class)){
					return "char("+cf.size()+")"+modifier;
				}
			}
			if(f.isAnnotationPresent(VarCharField.class)){
				VarCharField ccf = f.getAnnotation(VarCharField.class);
				if(f.getType().equals(String.class)){
					return "varchar("+ccf.size()+")"+modifier;
				}
			}
			if(f.isAnnotationPresent(DoubleField.class)){
				DoubleField df = f.getAnnotation(DoubleField.class);
				if(f.getType().equals(Double.TYPE)){
					return "decimal"+modifier;
				}
			}
			if(f.isAnnotationPresent(IntegerField.class)){
				IntegerField intf = f.getAnnotation(IntegerField.class);
				if(f.getType().equals(Integer.TYPE)){
					if(intf.Serial()){
						return "serial";
					}
					return "integer"+modifier;
				}
			}
			if(f.isAnnotationPresent(DateTimeField.class)){
				if(f.getType().equals(Date.class)){
					return "timestamp"+modifier;
				}
			}
			if(f.isAnnotationPresent(BooleanField.class)){
				BooleanField bf = f.getAnnotation(BooleanField.class);
				if(f.getType().equals(Boolean.TYPE)){
					return "boolean"+modifier;
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
	public static String convertToString(Object c){
		return new String(((ByteBuffer) c).array());
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
				if(f.getType().equals(Double.class) || f.getType().equals(Double.TYPE) ){
					return Double.parseDouble(new String(((ByteBuffer) c).array()));
				}
				if(f.getType().equals(Float.class) || f.getType().equals(Double.TYPE)){
					return Float.parseFloat(new String(((ByteBuffer) c).array()));
				}
			}
			if(f.isAnnotationPresent(IntegerField.class)){
				if(f.getType().equals(Integer.class) || f.getType().equals(Integer.TYPE)){
					int result = Integer.parseInt(new String(((ByteBuffer) c).array()));
					return result;
				}
			}
			if(f.isAnnotationPresent(DateTimeField.class)){
				if(f.getType().equals(Date.class)){
					String dateStr = new String(((ByteBuffer) c).array());
					if(dateStr.equals("None")){
						return null;
					}
					Date result = new Date(Date.parse(new String(((ByteBuffer) c).array())));
					return result;
				}
			}
			if(f.isAnnotationPresent(BooleanField.class)){
				if(f.getType().equals(Boolean.class) || f.getType().equals(Boolean.TYPE)){
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
