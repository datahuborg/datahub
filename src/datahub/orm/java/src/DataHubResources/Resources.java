package DataHubResources;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.nio.ByteBuffer;

import DataHubORM.DataHubConverter;

import datahub.DHType;

public class Resources {
	
	//TODO:implement SQL escape
	public static String sqlEscape(String query){
		return query;
	}
	public static <T,U> void setField(T object, String fieldName, U value){
		try{
			Field f = object.getClass().getField(fieldName);
			f.set(object, convert(value,f.getType()));
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public static <T> T fieldToInstance(Field f){
		try{
			return (T) f.getType().newInstance();
		}catch(Exception e){
			e.printStackTrace();
			return null;
		}
	}
	public static Object convert(Object c, Type t){
		if(t.equals(String.class)){
			return new String(((ByteBuffer) c).array());
		}
		return c;
	}
}
