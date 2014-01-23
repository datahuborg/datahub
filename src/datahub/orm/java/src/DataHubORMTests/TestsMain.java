package DataHubORMTests;

import java.util.Random;

import org.apache.thrift.TException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;
import Examples.TestDatabase;
import Examples.TestModel;
import datahub.DHException;

public class TestsMain {
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
			db.clearAndReCreate();
			//System.out.println("connected!");
			this.db = db;
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	@After
	public void tearDown(){
		db.disconnect();
	}
	public TestModel newTestModel() throws DataHubException{
		Random generator = new Random();
		String name = "test"+Math.abs(generator.nextInt());
		String description = "test row";
		TestModel t = new TestModel();
		t.name = name;
		t.description = description;
		return t;
	}
	
}
