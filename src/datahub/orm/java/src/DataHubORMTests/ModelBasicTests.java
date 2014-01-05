package DataHubORMTests;

import static org.junit.Assert.assertEquals;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.protocol.TTupleProtocol;
import org.apache.thrift.transport.TFastFramedTransport;
import org.apache.thrift.transport.TFramedTransport;
import org.apache.thrift.transport.THttpClient;
import org.apache.thrift.transport.TIOStreamTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubException;
import Examples.DeviceModel;
import Examples.TestModel;
import Examples.TesterModel;
import Examples.UserModel;

import datahub.DHCell;
import datahub.DHConnection;
import datahub.DHConnectionParams;
import datahub.DHException;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DataHub;
import datahub.DHConnectionParams._Fields;


public class ModelBasicTests extends TestsMain{
	
	//@Test
	public void testCreateAndDelete() throws DataHubException{
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		assertEquals(t.id!=0,true);
		
		HashMap<String, Object> params = new HashMap<String,Object>();
		params.put("id", t.id);
		TestModel t1 = this.db.test.findOne(params);
		assertEquals(t1!=null,true);
		assertEquals(t1.name,t.name);
		assertEquals(t1.description,t.description);
		
		
		t.destroy();
		TestModel t2 = this.db.test.findOne(params);
		
		assertEquals(t2==null,true);
	}
	//@Test
	public void testSave() throws DataHubException{
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
	//@Test
	public void testSave2ChangeObject() throws DataHubException{
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
		
		//System.out.println(d.testModel);
		
		d.testModel = t1;
		d.save();
		
		//System.out.println(t1);
		//System.out.println(d.testModel);
		
		assertEquals(d.testModel.equals(t1),true);
		assertEquals(d.testModel.equals(t),false);
		
		d.destroy();
		t1.destroy();
		t.destroy();
		
		System.out.println("hits"+db.hitCount);
		System.out.println("misses"+db.missCount);
	}
	//@Test
	public void testDataHubArrayList() throws DataHubException{
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
		
		System.out.println("hits"+db.hitCount);
		System.out.println("misses"+db.missCount);
	}
	//@Test
	public void testHasOneAndBelongsTo() throws DataHubException{
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
		
		assertEquals(tester.test.equals(t), true);
		
		tester.save();
		
		assertEquals(tester.id!=0,true);
		assertEquals(tester.test.equals(t), true);
		
		HashMap<String,Object> testerParams = new HashMap<String,Object>();
		testerParams.put("id", tester.id);
		TesterModel tester1 = db.testers.findOne(testerParams);
		HashMap<String,Object> testParams = new HashMap<String,Object>();
		testParams.put("id", t.id);
		TestModel test1 = db.test.findOne(testParams);
		
		assertEquals(tester1.test.equals(test1), true);
		assertEquals(test1.tester.equals(tester1), true);
		
		tester.destroy();
		t.destroy();
		
		System.out.println("hits"+db.hitCount);
		System.out.println("misses"+db.missCount);
	}
	@Test
	public void HABTMTest() throws DataHubException{
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		
		assertEquals(t.id!=0,true);
		
		UserModel u1 = new UserModel();
		u1.username = "david";
		u1.save();
		
		assertEquals(u1.id!=0,true);
		
		t.users.add(u1);
		t.save();
		
		System.out.println(t.users);
		
		HashMap<String,Object> testparams = new HashMap<String,Object>();
		testparams.put("id", t.id);
		
		HashMap<String,Object> userparams = new HashMap<String,Object>();
		userparams.put("id", u1.id);
		
		TestModel t1 = db.test.findOne(testparams);
		UserModel u2 = db.users.findOne(userparams);
		
		System.out.println(t1.users);
		System.out.println(u2.tests);
		
		t1.users.remove(u1);
		t1.save();
		
		System.out.println(t1.users);
		
		TestModel t2 = db.test.findOne(testparams);
		UserModel u3 = db.users.findOne(userparams);
		
		System.out.println(t2.users);
		System.out.println(u3.tests);
		
		//t.destroy();
		//u1.destroy();
		
		System.out.println("hits"+db.hitCount);
		System.out.println("misses"+db.missCount);
		
	}

}
