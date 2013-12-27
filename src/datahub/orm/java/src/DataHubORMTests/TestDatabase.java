package DataHubORMTests;

import Annotations.database;
import DataHubORM.Database;

@database(name="test")
public class TestDatabase extends Database {
	
	public TestModel test;	
	
}
