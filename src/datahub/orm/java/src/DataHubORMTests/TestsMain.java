package DataHubORMTests;

import java.util.Random;

import org.apache.thrift.TException;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;
import Examples.TestDatabase;
import Examples.TestModel;
import datahub.DHException;

public class TestsMain {
	public static DataHubAccount test_dha;
	public static TestDatabase db;
	
	@BeforeClass
	public static void setUp() throws DHException, TException, DataHubException{
		test_dha = new DataHubAccount("dggoeh1", new DataHubUser("dggoeh1@mit.edu","dggoeh1"));
		TestDatabase db1 = new TestDatabase();
		db1.setDataHubAccount(test_dha);
		try{
			//System.out.println("connecting!");
			db1.clearAndReCreate();
			//System.out.println("connected!");
			db = db1;
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	@AfterClass
	public static void tearDown(){
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
