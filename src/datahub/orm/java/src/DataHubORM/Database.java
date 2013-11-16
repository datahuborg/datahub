package DataHubORM;

import java.util.ArrayList;

import DataHubAccount.DataHubClient;

public class Database {
	
	//Initially assume all models are from only one database
	
	//every database will have this to store config information
	public Model DataHubBasicInfo;
	
	public String dbName;
	
	private DataHubClient dhc;
	
	public Database(String dbName){
		this.dbName = dbName;
	}
	public Database(String dbName, DataHubClient dhc) throws Exception{
		this.dbName = dbName;
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
