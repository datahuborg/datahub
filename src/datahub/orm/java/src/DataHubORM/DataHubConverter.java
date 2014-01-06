package DataHubORM;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import javax.print.DocFlavor.STRING;

import Annotations.association;
import Annotations.column;
import Annotations.column.Index;
import Annotations.table;
import DataHubResources.Constants;

import datahub.DHType;

public class DataHubConverter {

	public static ArrayList<HashMap<Class,HashMap<Field,DHType>>> convertDBToSchema(Database db){
		ArrayList<HashMap<Class,HashMap<Field,DHType>>> out = new ArrayList<HashMap<Class,HashMap<Field,DHType>>>();
		ArrayList<Field> models = findModels(db);
		for(Field model: models){
			out.add(extractColumnBasicFromClass(model.getType()));
		}
		return out;
	}
	public static ArrayList<Field> findModels(Database db){
		Field[] dbFields = db.getClass().getFields();
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
			if(c.equals(Model.class) || c.asSubclass(Model.class) != null){
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
					fieldsDHType.put(f, javaTypeToDHType(f.getType()));
					continue;
				}
			}
			if(hasAssociation(f)){
				if(!basic){
					fieldsDHType.put(f, javaTypeToDHType(f.getType()));
					continue;
				}
			}
		}
		//check for table annotation
		if(model.isAnnotationPresent(table.class)){
			try {
				//update table information
				tableName = ((table) model.getAnnotation(table.class)).name();
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
		if(f.isAnnotationPresent(column.class)){
			return true;
		}
		return false;
	}
	public static boolean hasAssociation(Field f){
		if(f.isAnnotationPresent(association.class)){
			return true;
		}
		return false;
	}
	public static DHType javaTypeToDHType(Type t){
		try{
			if(t.equals(Integer.TYPE)){
				return DHType.Integer;
			}
			if(t.equals(Boolean.TYPE)){
				return DHType.Boolean;
			}
			if(t.equals(String.class)){
				return DHType.Text;
			}
		}catch(Exception e){
			
		}
		return DHType.Binary;
	}
}
