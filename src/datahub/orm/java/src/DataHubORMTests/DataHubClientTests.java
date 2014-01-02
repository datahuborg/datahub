package DataHubORMTests;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import datahub.DHException;
import datahub.DataHub;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.Database;

public class DataHubClientTests {
	public DataHubAccount test_dha;
	public TestDatabase db;
	@Before
	public void setUp() throws DHException, TException{
		test_dha = new DataHubAccount("dggoeh1", new DataHubUser("dggoeh1@mit.edu","dggoeh1"));
		TestDatabase db = new TestDatabase();
		db.setDataHubAccount(this.test_dha);
		try{
			//System.out.println("connecting!");
			db.connect();
			//System.out.println("connected!");
			this.db = db;
		}catch(Exception e){
			
		}
	}
	
	@After
	public void tearDown(){
		db.disconnect();
	}
	
	@Test
	public void testCreateAndDelete(){
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		assertEquals(t.id!=0,true);
		
		HashMap<String, Object> params = new HashMap<String,Object>();
		params.put("name", name);
		TestModel t1 = this.db.test.findOne(params);
		assertEquals(t1!=null,true);
		assertEquals(t1.name,t.name);
		assertEquals(t1.description,t.description);
		
		
		t.destroy();
		TestModel t2 = this.db.test.findOne(params);
		assertEquals(t2==null,true);
	}
	@Test
	public void testSave(){
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		assertEquals(t.id!=0,true);
		
		int id = t.id;
		HashMap<String, Object> params = new HashMap<String,Object>();
		params.put("id", id);
		
		//verify creation
		TestModel t1 = this.db.test.findOne(params);
		assertEquals(t1!=null,true);
		assertEquals(t1.name,t.name);
		assertEquals(t1.description,t.description);
		
		//change stuff
		String newName = "lol";
		String newDescription = "he-llo-o";
		t.name = "lol";
		t.description = "he-llo-o";
		t.save();

		TestModel t2 = this.db.test.findOne(params);
		assertEquals(t2!=null,true);
		assertEquals(t2.id==t.id,true);
		assertEquals(t2.name,newName);
		assertEquals(t2.description,newDescription);
		
		t.destroy();
		TestModel t3 = this.db.test.findOne(params);
		assertEquals(t3==null,true);
	}
	@Test
	public void testSave2ChangeObject(){
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		assertEquals(t.id!=0,true);
		
		String name1 = "test"+Math.abs(generator.nextInt());
		String description1 = "test row";
		TestModel t1 = new TestModel();
		t1.name = name1;
		t1.description = description1;
		t1.save();
		assertEquals(t1.id!=0,true);

		String code = "test_code"+Math.abs(generator.nextInt());
		DeviceModel d = new DeviceModel();
		d.code = code;
		d.testModel = t;
		d.save();
		assertEquals(d.id!=0,true);
		
		
		assertEquals(d.testModel.equals(t),true);
		
		d.testModel = t1;
		d.save();
		assertEquals(d.testModel.equals(t1),true);
		assertEquals(d.testModel.equals(t),false);
		
		d.destroy();
		t1.destroy();
		t.destroy();
		
	}
	@Test
	public void testDataHubArrayList(){
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		assertEquals(t.id!=0,true);
		
		String code = "test_code"+Math.abs(generator.nextInt());
		DeviceModel d = new DeviceModel();
		d.code = code;
		d.save();
		assertEquals(d.id!=0,true);
		
		//add device
		t.devices.add(d);
		
		
		//did not save, make sure object has no devices
		int id = t.id;
		HashMap<String, Object> params = new HashMap<String,Object>();
		params.put("id", id);
		TestModel t1 = db.test.findOne(params);
		
		assertEquals(t1.devices.size()==0,true);
		
		
		//now save and make sure object has one device
		t.save();
		TestModel t2 = db.test.findOne(params);
		
		assertEquals(t2.devices.size()==1,true);
		
		//now test remove
		t.devices.remove(d);
		TestModel t3 = db.test.findOne(params);
		
		assertEquals(t.devices.contains(d), false);
		assertEquals(t3.devices.contains(d),true);
		
		t.save();
		TestModel t4 = db.test.findOne(params);
		
		//System.out.println("TESTMODEL");
		//System.out.println(t);
		//System.out.println("DEVICES");
		//System.out.println(t4.devices);
		assertEquals(t4.devices.contains(d),false);
		
		d.destroy();
		t.destroy();
	}
	@Test
	public void testHasOneAndBelongsTo(){
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		
		assertEquals(t.id!=0,true);
		assertEquals(t.tester==null, true);
		
		String testername = "tester"+Math.abs(generator.nextInt());
		TesterModel tester = new TesterModel();
		tester.testerName = testername;
		tester.test = t;
		tester.save();
		
		assertEquals(tester.id!=0,true);
		
		HashMap<String,Object> testerParams = new HashMap<String,Object>();
		testerParams.put("id", tester.id);
		TesterModel tester1 = db.testers.findOne(testerParams);
		HashMap<String,Object> testParams = new HashMap<String,Object>();
		testerParams.put("id", t.id);
		TestModel test1 = db.test.findOne(testerParams);
		
		assertEquals(tester1.test.equals(test1), true);
		assertEquals(test1.tester.equals(tester1), true);
		
		
		
		
	}
	
	@Test
	public void basicTest(){
      TTransport transport = new TSocket(
                 "datahub-experimental.csail.mit.edu", 9000);
      try {
		transport.open();
		
		    
		TProtocol protocol = new TBinaryProtocol(transport);
		DataHub.Client client = new DataHub.Client(protocol);
		
		System.out.println(client.get_version());
		transport.close();
      }catch(Exception e){
    	  
      }
	}
	@Test
	public void testGetSchema(){
		TestDatabase db = new TestDatabase();
		db.setDataHubAccount(this.test_dha);
		try{
			db.connect();
			TestModel.setDatabase(db);
			/*for(int i=0; i<10; i++){
				TestModel t = new TestModel();
				t.name = i+"";
				t.description = i+"s description";
				t.save();
			}*/
			//ArrayList<TestModel> results = db.test.findAll();
			HashMap<String, Object> params = new HashMap<String,Object>();
			params.put("id", "477");
			ArrayList<TestModel> results = db.test.findAll(params);
			for(TestModel m1: results){
				System.out.println("id"+m1.id);
				System.out.println("name"+m1.name);
				System.out.println(m1.description);
				System.out.println(m1.devices);
				ArrayList<DeviceModel> devices1 = (ArrayList<DeviceModel>) m1.devices.clone();
				for(DeviceModel d:devices1){
					System.out.println("code"+d.code);
					System.out.println("testModel id"+d.testModel.id);
					System.out.println("testModel name"+d.testModel.name);
					System.out.println("testModel description"+d.testModel.description);
					m1.devices.remove(d);
				}
				/*DeviceModel d1 = new DeviceModel();
				d1.code = "f12a";
				m1.devices.add(d1);
				m1.save();*/
				//System.out.println(m1.findAll());
				//System.out.println(m1.generateSQLRep());
				//m1.description = "lol";
				//m1.save();
				//m1.destroy();
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}

}
