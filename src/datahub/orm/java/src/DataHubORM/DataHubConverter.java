package DataHubORM;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.util.ArrayList;
import java.util.HashMap;

import DataHubResources.Constants;

import datahub.DHType;

public class DataHubConverter {

	public static ArrayList<HashMap<String,ArrayList<HashMap<String,String>>>> convertDBToSchema(Database db){
		ArrayList<HashMap<String,ArrayList<HashMap<String,String>>>> out = new ArrayList<HashMap<String,ArrayList<HashMap<String,String>>>> ();
		return out;
	}
	public static <T extends Database> ArrayList<Field> findModels(T db){
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
	public static HashMap<String,HashMap<String,DHType>> extractDataFromClass(Class<? extends Model> model){
		HashMap<String,HashMap<String,DHType>> output = new HashMap<String,HashMap<String,DHType>>();
		HashMap<String,DHType> fieldsDHType = new HashMap<String,DHType>();
		Field[] fields = model.getFields();
		String tableName = "Lol";
		for(Field f:fields){
			if(f.getType().equals(Column.class)){
				//f.getGenericType()
				fieldsDHType.put(f.getName(), javaTypeToDHType(f.getGenericType()));
			}
			if(f.getName().equals(Constants.MODEL_TABLE_NAME_ATTRIBUTE)){
				try {
					if(f.get(null) != null){
						tableName = f.get(null).toString();
					}
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		if(tableName != null){
			output.put(tableName, fieldsDHType);
		}
		return output;
	}
	public static DHType javaTypeToDHType(Type t){
		try{
			if(t.equals(Constants.class.getField(Constants.integerColumnName).getGenericType())){
				return DHType.Integer;
			}
			if(t.equals(Constants.class.getField(Constants.integerColumnName).getGenericType())){
				return DHType.Boolean;
			}
		}catch(Exception e){
			
		}
		return DHType.Binary;
	}
}
