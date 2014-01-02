package DataHubORMTests;

import Annotations.column;
import Annotations.column.Index;
import Annotations.column.RelationType;
import Annotations.table;
import DataHubORM.DataHubArrayList;
import DataHubORM.Model;

@table(name="test")
public class TestModel extends Model<TestModel> {
	
	@column(name="name")
	public String name;
	
	@column(name="description") 
	public String description;
	
	@column(name="test_id",Index=Index.ForeignKey, RelationType=RelationType.HasOne)
	public TesterModel tester;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@column(name="test_id",Index=Index.ForeignKey,RelationType=RelationType.HasMany)
	public DevicesDataHubArrayList devices;

}
