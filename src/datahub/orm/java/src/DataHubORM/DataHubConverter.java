package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;

import datahub.DHType;

public class DataHubConverter {

	public static ArrayList<HashMap<String,ArrayList<HashMap<String,String>>>> convertDBToSchema(Database db){
		ArrayList<HashMap<String,ArrayList<HashMap<String,String>>>> out = new ArrayList<HashMap<String,ArrayList<HashMap<String,String>>>> ();
		return out;
	}
	public static ArrayList<Field> findModels(Database db){
		Field[] dbFields = db.getClass().getFields();
		ArrayList<Field> modelFields = new ArrayList<Field>();
		for(Field f:dbFields){
			try{
				if(f.getType().equals(Model.class) || f.getType().asSubclass(Model.class) != null){
					modelFields.add(f);
				}
			}catch(Exception e){
				
			}
		}
		return modelFields;
	}
	public static HashMap<String,HashMap<String,DHType>> extractDataFromClass(Field model){
		HashMap<String,HashMap<String,DHType>> output = new HashMap<String,HashMap<String,DHType>>();
		HashMap<String,DHType> fieldsDHType = new HashMap<String,DHType>();
		Field[] fields = model.getType().getFields();
		for(Field f:fields){
			fieldsDHType.put(f.getName(), javaTypeToDHType(f));
		}
		output.put(model.getName(), fieldsDHType);
		return output;
	}
	public static DHType javaTypeToDHType(Field f){
		if(f.getType().equals(Integer.class)){
			return DHType.Integer;
		}
		if(f.getType().equals(Integer.class)){
			return DHType.Boolean;
		}
		return DHType.Binary;
	}
}
