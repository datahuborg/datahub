package DataHubORMTests;

import static org.junit.Assert.*;

import java.util.ArrayList;
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
import DataHubAccount.DataHubClient;
import DataHubAccount.DataHubUser;
import DataHubORM.Database;

public class DataHubClientTests {
	public DataHubAccount test_dha;
	public DataHubClient test_dhc;
	
	@Before
	public void setUp() throws DHException, TException{
		test_dha = new DataHubAccount("dggoeh1", new DataHubUser("dggoeh1@mit.edu","dggoeh1"));
		test_dhc = new DataHubClient(test_dha);
	}
	
	@After
	public void tearDown(){
		test_dhc.disconnect();
	}
	/*@Test
	public void testExists() throws Exception {
		TestDatabase bdb1 = new TestDatabase();
		TestDatabase bdb2 = new TestDatabase("test2");
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
	}*/
	//@Test
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
			//test_dhc.connect(bdb1);
			//System.out.println(test_dhc.getDatabaseSchema());
			//System.out.println(test_dhc.getDatabaseSchema().data.schema.fields);
			db.connect();
			for(int i=0; i<10; i++){
				TestModel t = new TestModel();
				t.setDatabase(db);
				t.name = i+"";
				t.description = i+"s description";
				t.save();
			}
			ArrayList<TestModel> results = db.test.findAll();
			for(TestModel m1: results){
				System.out.println(m1.id);
				System.out.println(m1.name);
				System.out.println(m1.description);
				System.out.println(m1.findAll());
				System.out.println(m1.generateSQLRep());
				m1.description = "lol";
				m1.save();
				m1.destroy();
			}
		}catch(Exception e){
			e.printStackTrace();
		}
	}

}
