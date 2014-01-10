package DataHubORMTests;

import static org.junit.Assert.*;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;

import org.junit.Test;

import DataHubORM.DataHubConverter;
import DataHubORM.DataHubDatabase;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;
import Examples.DeviceModel;
import Examples.TestDatabase;
import Examples.TestModel;

public class DataHubConverterTests {

	//@Test
	public void testFindModelFields() {
		TestDatabase db = new TestDatabase();
		ArrayList<Field> fields = DataHubConverter.findModels(db.getClass());
		System.out.println(fields);
	}
	
	//@Test
	public void testextractDataFromClass(){
		TestDatabase db = new TestDatabase();
		System.out.println(DataHubConverter.convertDBToSchema(db.getClass()));
	}
	@Test
	public void testModelBasicToSQL() throws DataHubException{
		TestDatabase db = new TestDatabase();
		System.out.println(DataHubConverter.convertModelBasicTOSQLSchemaString(TestModel.class));
	}
	@Test
	public void testDatabaseToSQL() throws DataHubException{
		TestDatabase db = new TestDatabase();
		System.out.println(DataHubConverter.convertDBToSQLSchemaString(db.getClass()));
	}
	//@Test
	//public void testGetSchema(){
	//	TestDatabase db = new TestDatabase();
	//	db.setDataHubAccount(this.test_dha);
	//	try{
	//		db.connect();
	//		TestModel.setDatabase(db);
	//		/*for(int i=0; i<10; i++){
	//			TestModel t = new TestModel();
	//			t.name = i+"";
	//			t.description = i+"s description";
	//			t.save();
	//		}*/
	//		//ArrayList<TestModel> results = db.test.findAll();
	//		HashMap<String, Object> params = new HashMap<String,Object>();
	//		params.put("id", "477");
	//		ArrayList<TestModel> results = db.test.findAll(params);
	//		for(TestModel m1: results){
	//			System.out.println("id"+m1.id);
	//			System.out.println("name"+m1.name);
	//			System.out.println(m1.description);
	//			System.out.println(m1.devices);
	//			ArrayList<DeviceModel> devices1 = (ArrayList<DeviceModel>) m1.devices.clone();
	//			for(DeviceModel d:devices1){
	//				System.out.println("code"+d.code);
	//				System.out.println("testModel id"+d.testModel.id);
	//				System.out.println("testModel name"+d.testModel.name);
	//				System.out.println("testModel description"+d.testModel.description);
	//				m1.devices.remove(d);
	//			}
				/*DeviceModel d1 = new DeviceModel();
				d1.code = "f12a";
				m1.devices.add(d1);
				m1.save();*/
				//System.out.println(m1.findAll());
				//System.out.println(m1.generateSQLRep());
				//m1.description = "lol";
				//m1.save();
				//m1.destroy();
	//		}
	//	}catch(Exception e){
	//		e.printStackTrace();
	//	}
	//}
}
