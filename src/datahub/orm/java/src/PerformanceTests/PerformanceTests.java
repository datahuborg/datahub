package PerformanceTests;

import static org.junit.Assert.*;

import org.apache.thrift.TException;
import org.junit.BeforeClass;
import org.junit.Test;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubException;
import Examples.TestDatabase;
import datahub.DHException;

public class PerformanceTests {
	public static DataHubAccount test_dha;
	public static PerformanceTestDB db;
	
	@BeforeClass
	public static void setUp() throws DHException, TException, DataHubException{
		test_dha = new DataHubAccount("dggoeh1", new DataHubUser("dggoeh1@mit.edu","dggoeh1"));
		PerformanceTestDB db1 = new PerformanceTestDB();
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
	@Test
	public void test() {
		fail("Not yet implemented");
	}

}
