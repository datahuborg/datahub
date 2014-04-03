package Examples;

import DataHubAnnotations.AnnotationsConstants;
import DataHubAnnotations.Database;
import DataHubORM.DataHubDatabase;
import DataHubORM.DataHubException;


@Database(setupMode=AnnotationsConstants.SetupModes.Manual,name="test")
public class TestDatabase extends DataHubDatabase {
	
	public TestDatabase() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	public TestModel test;	
	
	public DeviceModel devices;
	
	public UserModel users;
	
	public TesterModel testers;
	
	public CarModel cars;
	
}
