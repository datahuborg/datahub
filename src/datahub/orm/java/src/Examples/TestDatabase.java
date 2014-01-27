package Examples;

import DataHubAnnotations.AnnotationsConstants;
import DataHubAnnotations.Database;
import DataHubORM.DataHubDatabase;


@Database(setupMode=AnnotationsConstants.SetupModes.Manual,name="test")
public class TestDatabase extends DataHubDatabase {
	
	public TestModel test;	
	
	public DeviceModel devices;
	
	public UserModel users;
	
	public TesterModel testers;
	
	public CarModel cars;
	
}
