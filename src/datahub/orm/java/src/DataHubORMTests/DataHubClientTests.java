package DataHubORMTests;

import static org.junit.Assert.*;

import java.util.Random;

import org.apache.thrift.TException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import datahub.DHException;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubClient;
import DataHubAccount.DataHubUser;
import DataHubORM.Database;

public class DataHubClientTests {
	public DataHubAccount test_dha;
	public DataHubClient test_dhc;
	
	@Before
	public void setUp() throws DHException, TException{
		test_dha = new DataHubAccount("dggoeh1", new DataHubUser("postgres","dggoeh1"));
		test_dhc = new DataHubClient(test_dha);
		test_dhc.connect();
	}
	
	@After
	public void tearDown(){
		test_dhc.disconnect();
	}
	@Test
	public void testExists() throws Exception {
		Database bdb1 = new Database("test");
		Database bdb2 = new Database("test2");
		assertEquals(true, test_dhc.databaseExists(bdb1));
		assertEquals(false, test_dhc.databaseExists(bdb2));
	}
	@Test
	public void testCreateAndDropDB() throws Exception{
		Random generator = new Random();
		Database bdb = new Database("test"+Math.abs(generator.nextInt()));
		test_dhc.createDatabase(bdb);
		assertEquals(true, test_dhc.databaseExists(bdb));
		test_dhc.dropDatabase(bdb);
		assertEquals(false, test_dhc.databaseExists(bdb));
	}
	@Test
	public void testGetSchema(){
		Database bdb1 = new Database("test");
		try {
			test_dhc.updateSchema(bdb1);
		} catch(Exception e){
			e.printStackTrace();
		}
	}

}
