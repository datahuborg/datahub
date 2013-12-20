package DataHubORMTests;

import Annotations.column;
import Annotations.table;
import DataHubORM.Model;

@table(name="test")
public class TestModel extends Model<TestModel> {
	
	@column(name="name")
	public String name;
	
	@column(name="description") 
	public String description;

}
