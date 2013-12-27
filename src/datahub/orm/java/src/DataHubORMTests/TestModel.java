package DataHubORMTests;

import Annotations.column;
import Annotations.column.Index;
import Annotations.table;
import DataHubORM.DataHubArrayList;
import DataHubORM.Model;

@table(name="test")
public class TestModel extends Model<TestModel> {
	
	@column(name="name")
	public String name;
	
	@column(name="description") 
	public String description;
	
	@column(Index=Index.LinkedSet)
	public DataHubArrayList<DeviceModel> devices;

}
