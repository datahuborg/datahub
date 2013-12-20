package DataHubORMTests;

import Annotations.database;
import DataHubAccount.DataHubClient;
import DataHubORM.Database;

@database(name="test")
public class TestDatabase extends Database {
	
	public TestModel test;	
	
}
