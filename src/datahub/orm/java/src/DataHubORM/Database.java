package DataHubORM;

import java.util.ArrayList;

import DataHubAccount.DataHubClient;

public class Database {
	
	public static String dbName;
	
	private DataHubClient dhc;
	
	public Database(){
		
	}
	
	public Database(DataHubClient dhc) throws Exception{
		this.dhc = dhc;
		initialize();
	}
	public String getDatabaseName(){
		return dbName;
	}
	private void initialize() throws Exception{
		dhc.connectToDatabase(this);
		//dhc.updateSchema(this);
	}
	
}
