package DataHubResources;

import java.lang.reflect.Field;
import java.lang.reflect.Type;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Iterator;

import DataHubORM.DataHubConverter;

import datahub.DHType;

public class Resources {
	public static <Q> String converToSQLAndConcatenate(Iterable<Q> i, String linkSymbol){
		ArrayList<String> sqlVersions = new ArrayList<String>();
		for(Q object: i){
			String objStr = Resources.objectToSQL(object);
			sqlVersions.add(objStr);
		}
		return Resources.concatenate(sqlVersions,linkSymbol);
	}
	public static <Q> String concatenate(Iterable<Q> i, String linkSymbol){
		String out = "";
		Iterator<Q> p = i.iterator();
		while(p.hasNext()){
			String strToAdd = p.next().toString();
			if(!strToAdd.equals("") && strToAdd!=null){
				out+=strToAdd;
				if(p.hasNext()){
					out+=" "+linkSymbol+" ";
				}
			}
		}
		return out;
	}
	//TODO:implement SQL escape
	public static String sqlEscape(String query){
		return query;
	}
	public static <T,U> void convertAndSetField(T object, String fieldName, U value){
		try{
			Field f = object.getClass().getField(fieldName);
			Object val = DataHubConverter.convertToJavaType(value, f);
			f.set(object, val);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	public static <T,U> void setField(T object, String fieldName, U value){
		try{
			Field f = object.getClass().getField(fieldName);
			f.set(object, value);
		}catch(Exception e){
			e.printStackTrace();
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
	public static Field getField(Class c, String field){
		Field out =  null;
		try{
			out = c.getField(field);
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
	public static String getFieldSQLStringRep(Object o, String field){
		String out = "";
		try{
			Object o1 = o.getClass().getField(field).get(o);
			out=objectToSQL(o1);
		}catch(Exception e){
			e.printStackTrace();
		}
		return out;
	}
	public static String objectToSQL(Object o1){
		String out = "";
		if(o1==null){
			return "NULL";
		}
		if(o1.getClass().equals(String.class)){
			out = "'"+o1.toString()+"'";
		}else{
			out = o1.toString();
		}
		return out;
	}
	public static String objectToSQLModifier(Object o1, boolean query){
		String out = "";
		if(query){
			if(o1==null){
				out = " is ";
			}else{
				out = "=";
			}
		}else{
			out="=";
		}
		return out;
	}
	public static boolean isNumeric(Class c){
		if(c.equals(Integer.class) || c.equals(Integer.TYPE) ||
		   c.equals(Double.class) || c.equals(Double.TYPE) ||
		   c.equals(Float.class) || c.equals(Float.TYPE) ||
		   c.equals(Short.class) || c.equals(Short.TYPE)){
			return true;
		}
		return false;
	}
}
