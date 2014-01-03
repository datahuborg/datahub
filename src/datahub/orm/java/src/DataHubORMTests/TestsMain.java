package DataHubORMTests;

import org.apache.thrift.TException;
import org.junit.After;
import org.junit.Before;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import Examples.TestDatabase;
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
			//System.out.println("connected!");
			this.db = db;
		}catch(Exception e){
			
		}
	}
	
	@After
	public void tearDown(){
		db.disconnect();
	}
}
