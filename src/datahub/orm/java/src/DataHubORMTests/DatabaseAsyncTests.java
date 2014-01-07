package DataHubORMTests;

import org.junit.Test;

import Workers.GenericCallback;

import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubUser;
import DataHubORM.DataHubException;
import Examples.TestDatabase;

public class DatabaseAsyncTests {

	@Test
	public void testConnectDB() throws InterruptedException{
		DataHubAccount test_dha = new DataHubAccount("dggoeh1", new DataHubUser("dggoeh1@mit.edu","dggoeh1"));
		final TestDatabase db = new TestDatabase();
		db.setDataHubAccount(test_dha);
		try{
			
			db.connectAsync(new GenericCallback<Void>(){

				@Override
				public void call(Void data) throws DataHubException {
					// TODO Auto-generated method stub
					System.out.println("Connected Successfully!");
					db.disconnectAsync(new GenericCallback<Void>(){
						@Override
						public void call(Void data) throws DataHubException {
							// TODO Auto-generated method stub
							System.out.println("Disconnected Successfully!");
						}});
					
				}});
		}catch(Exception e){
			System.out.println("Failed to connect!");
		}
		Thread.sleep(1000);
		
	}
	
}
