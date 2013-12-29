package DataHubORM;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import javax.print.DocFlavor.STRING;

import Annotations.column;
import Annotations.column.Index;
import Annotations.table;
import DataHubResources.Constants;

import datahub.DHType;

public class DataHubConverter {

	public static ArrayList<HashMap<String,HashMap<String,DHType>>> convertDBToSchema(Database db){
		ArrayList<HashMap<String,HashMap<String,DHType>>> out = new ArrayList<HashMap<String,HashMap<String,DHType>>>();
		ArrayList<Field> models = findModels(db);
		for(Field model: models){
			out.add(extractDataFromClass(model.getType()));
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
	public static HashMap<String,HashMap<String,DHType>> extractDataFromClass(Class model){
		
		//TODO: do model type checks here
		
		//output hashmaps
		HashMap<String,HashMap<String,DHType>> output = new HashMap<String,HashMap<String,DHType>>();
		HashMap<String,DHType> fieldsDHType = new HashMap<String,DHType>();
		
		//model fields
		Field[] fields = model.getDeclaredFields();
		
		//table annotation detection
		int tableCount = 0;
		String tableName = null;
		
		//iterate over all fields
		for(Field f:fields){
			//check for column annotation
			if(hasColumnBasic(f)){
				fieldsDHType.put(f.getName(), javaTypeToDHType(f.getType()));
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
			output.put(tableName, fieldsDHType);
		}
		return output;
	}
	public static boolean hasColumnBasic(Field f){
		if(f.isAnnotationPresent(column.class) && f.getAnnotation(column.class).Index() != Index.HasMany){
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
