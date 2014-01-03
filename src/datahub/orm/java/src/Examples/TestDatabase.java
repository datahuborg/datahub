package Examples;

import Annotations.database;
import DataHubORM.Database;

@database(name="test")
public class TestDatabase extends Database {
	
	public TestModel test;	
	
	public DeviceModel devices;
	
	public UserModel users;
	
	public TesterModel testers;
	
}
