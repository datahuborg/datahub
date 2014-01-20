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
		db.resetStats();
		
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
		db.resetStats();
		
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		assertEquals(t.id!=0,true);
		
		db.printStats();
		
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
		
		db.printStats();
	}
	//@Test
	public void testSave2ChangeObject() throws DataHubException{
		db.resetStats();
		
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
		
		db.printStats();
	}
	//@Test
	public void testDataHubArrayList() throws DataHubException{
		db.resetStats();
		
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
		
		db.printStats();
	}
	//@Test
	public void testHasOneAndBelongsTo() throws DataHubException{
		db.resetStats();
		
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
		
		db.printStats();
	}
	//@Test
	public void HABTMTest() throws DataHubException{
		db.resetStats();
		
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		
		String name1 = "test"+Math.abs(generator.nextInt());
		String description1 = "test row1234567";
		TestModel t1 = new TestModel();
		t1.name = name1;
		t1.description = description1;
		t1.save();
		
		UserModel u1 = new UserModel();
		u1.username = "david1";
		u1.save();
		
		UserModel u2 = new UserModel();
		u2.username = "david2";
		u2.save();
		
		UserModel u3 = new UserModel();
		u3.username = "david3";
		u3.save();
		
		
		t.users.add(u1);
		t.users.add(u2);
		t.save();
		
		t1.users.add(u2);
		t1.users.add(u3);
		t1.save();
		
		assertEquals(t.users.contains(u1), true);
		assertEquals(t.users.contains(u2), true);
		assertEquals(t.users.contains(u3), false);
		assertEquals(t1.users.contains(u1), false);
		assertEquals(t1.users.contains(u2), true);
		assertEquals(t1.users.contains(u3), true);
		
		HashMap<String,Object> testparams = new HashMap<String,Object>();
		testparams.put("id", t.id);
		
		HashMap<String,Object> test1params = new HashMap<String,Object>();
		test1params.put("id", t1.id);
		
		HashMap<String,Object> user1params = new HashMap<String,Object>();
		user1params.put("id", u1.id);
		
		HashMap<String,Object> user2params = new HashMap<String,Object>();
		user2params.put("id", u2.id);
		
		HashMap<String,Object> user3params = new HashMap<String,Object>();
		user3params.put("id", u3.id);
		
		TestModel refreshedT = db.test.findOne(testparams);
		TestModel refreshedT1 = db.test.findOne(test1params);
		
		assertEquals(refreshedT.users.contains(u1), true);
		assertEquals(refreshedT.users.contains(u2), true);
		assertEquals(refreshedT.users.contains(u3), false);
		assertEquals(refreshedT1.users.contains(u1), false);
		assertEquals(refreshedT1.users.contains(u2), true);
		assertEquals(refreshedT1.users.contains(u3), true);
		
		UserModel refreshedU1 = db.users.findOne(user1params);
		UserModel refreshedU2 = db.users.findOne(user2params);
		UserModel refreshedU3 = db.users.findOne(user3params);
		
		assertEquals(refreshedU1.tests.contains(t), true);
		assertEquals(refreshedU1.tests.contains(t1), false);
		assertEquals(refreshedU2.tests.contains(t), true);
		assertEquals(refreshedU2.tests.contains(t1), true);
		assertEquals(refreshedU3.tests.contains(t), false);
		assertEquals(refreshedU3.tests.contains(t1), true);
		
		t.users.remove(u1);
		t1.users.remove(u3);
		t.save();
		t1.save();
		
		TestModel refreshed1T = db.test.findOne(testparams);
		TestModel refreshed1T1 = db.test.findOne(test1params);
		
		assertEquals(refreshed1T.users.contains(u1), false);
		assertEquals(refreshed1T.users.contains(u2), true);
		assertEquals(refreshed1T.users.contains(u3), false);
		assertEquals(refreshed1T1.users.contains(u1), false);
		assertEquals(refreshed1T1.users.contains(u2), true);
		assertEquals(refreshed1T1.users.contains(u3), false);
		
		UserModel refreshed1U1 = db.users.findOne(user1params);
		UserModel refreshed1U2 = db.users.findOne(user2params);
		UserModel refreshed1U3 = db.users.findOne(user3params);
		
		assertEquals(refreshed1U1.tests.contains(t), false);
		assertEquals(refreshed1U1.tests.contains(t1), false);
		assertEquals(refreshed1U2.tests.contains(t), true);
		assertEquals(refreshed1U2.tests.contains(t1), true);
		assertEquals(refreshed1U3.tests.contains(t), false);
		assertEquals(refreshed1U3.tests.contains(t1), false);
		
		u2.tests.remove(t);
		u2.tests.remove(t1);
		u2.save();
		
		TestModel refreshed2T = db.test.findOne(testparams);
		TestModel refreshed2T1 = db.test.findOne(test1params);
		
		assertEquals(refreshed2T.users.contains(u1), false);
		assertEquals(refreshed2T.users.contains(u2), false);
		assertEquals(refreshed2T.users.contains(u3), false);
		assertEquals(refreshed2T1.users.contains(u1), false);
		assertEquals(refreshed2T1.users.contains(u2), false);
		assertEquals(refreshed2T1.users.contains(u3), false);
		
		UserModel refreshed2U1 = db.users.findOne(user1params);
		UserModel refreshed2U2 = db.users.findOne(user2params);
		UserModel refreshed2U3 = db.users.findOne(user3params);
		
		assertEquals(refreshed2U1.tests.contains(t), false);
		assertEquals(refreshed2U1.tests.contains(t1), false);
		assertEquals(refreshed2U2.tests.contains(t), false);
		assertEquals(refreshed2U2.tests.contains(t1), false);
		assertEquals(refreshed2U3.tests.contains(t), false);
		assertEquals(refreshed2U3.tests.contains(t1), false);
		
		
		t.destroy();
		t1.destroy();
		u1.destroy();
		u2.destroy();
		u3.destroy();
		
		db.printStats();
	}
	//@Test
	public void testQueryByObject() throws DataHubException{
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		t.save();
		
		String name1 = "test"+Math.abs(generator.nextInt());
		String description1 = "test row123123";
		TestModel t1 = new TestModel();
		t1.name = name1;
		t1.description = description1;
		t1.save();
		
		assertEquals(t.id!=0,true);
		assertEquals(t1.id!=0,true);
		
		UserModel u1 = new UserModel();
		u1.username = "david";
		u1.save();
		
		assertEquals(u1.id!=0,true);
		
		//t.users.add(u1);
		//t1.users.add(u1);
		
		t.save();
		t1.save();
		
		TesterModel testerM = new TesterModel();
		testerM.testerName="lol1234";
		testerM.test = t;
		testerM.save();
		
		assertEquals(testerM.id!=0,true);
		
		String code = "test_code"+Math.abs(generator.nextInt());
		DeviceModel d = new DeviceModel();
		d.code = code;
		d.save();
		
		String code1 = "test_code1234"+Math.abs(generator.nextInt());
		DeviceModel d1 = new DeviceModel();
		d1.code = code1;
		d1.save();
		
		assertEquals(d.id!=0,true);
		assertEquals(d1.id!=0,true);
		
		t.devices.add(d);
		t.devices.add(d1);
		t.save();
		
		HashMap<String,Object> params = new HashMap<String,Object>();
		params.put("tester", testerM);
		TestModel test =db.test.findOne(params);
		
		HashMap<String,Object> params1 = new HashMap<String,Object>();
		params1.put("test", t);
		TesterModel tester = db.testers.findOne(params1);
		
		/*HashMap<String,Object> params2 = new HashMap<String,Object>();
		params2.put("users", u1);
		ArrayList<TestModel> tests = db.test.findAll(params2);
		
		System.out.println(tests);*/
		
		assert(tester.test.equals(test));
		assert(test.tester.equals(tester));
		
		
		d.destroy();
		d1.destroy();
		testerM.destroy();
		u1.destroy();
		t.destroy();
		t1.destroy();
		
	}
	@Test 
	public void createTest() throws DataHubException{
		db.resetStats();
		ArrayList<TestModel> tms = new ArrayList<TestModel>();
		ArrayList<UserModel> ums = new ArrayList<UserModel>();
		for(int j = 1; j<10; j++){
			UserModel u = new UserModel();
			u.username="user"+j;
			u.save();
			ums.add(u);
		}
		for(int i = 0; i<30; i++){
			TestModel t = this.newTestModel();
			for(UserModel u: ums){
				t.users.add(u);
			}
			t.save();
			tms.add(t);
		}
		HashMap<String,Object> params = new HashMap<String,Object>();
		params.put("id", tms.get(0).id);
		TestModel t1 = db.test.findOne(params);
		System.out.println(t1);
		db.printStats();
		t1.destroy();
	}
	//@Test
	public void testQueryWithModifiers(){
		
	}
}
