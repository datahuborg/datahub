package DataHubResources;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.math.BigInteger;
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
			//e.printStackTrace();
		}
	}
	public static boolean hasField(Class c, String field){
		boolean out =  false;
		try{
			c.getField(field);
			out = true;
		}catch(Exception e){
			
		}
		return out;
	}
	public static <T> T fieldToInstance(Field f){
		try{
			return (T) f.getType().newInstance();
		}catch(Exception e){
			e.printStackTrace();
			return null;
		}
	}
	public static String getFieldStringRep(Object o, String field){
		String out = "";
		try{
			Object o1 = o.getClass().getField(field).get(o);
			out=o1.toString();
		}catch(Exception e){
			
		}
		return out;
	}
	public static String objectToSQL(Object o1){
		String out = "";
		if(o1.getClass().equals(String.class)){
			out = "'"+o1.toString()+"'";
		}else{
			out = o1.toString();
		}
		return out;
	}
	public static Object convert(Object c, Type t){
		if(t.equals(String.class)){
			return new String(((ByteBuffer) c).array());
		}
		if(t.equals(Integer.TYPE)){
			int result = Integer.parseInt(new String(((ByteBuffer) c).array()));
			return result;
		}
		return c;
	}
}
