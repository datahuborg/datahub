package Examples;

import DataHubAnnotations.Database;
import DataHubORM.DataHubDatabase;


@Database(name="test")
public class TestDatabase extends DataHubDatabase {
	
	public TestModel test;	
	
	public DeviceModel devices;
	
	public UserModel users;
	
	public TesterModel testers;
	
}
