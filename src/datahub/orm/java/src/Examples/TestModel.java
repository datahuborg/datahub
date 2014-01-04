package Examples;

import Annotations.column;
import Annotations.column.Index;
import Annotations.column.AssociationType;
import Annotations.table;
import DataHubORM.DataHubArrayList;
import DataHubORM.DataHubException;
import DataHubORM.Model;

@table(name="test")
public class TestModel extends Model<TestModel> {
	
	public TestModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@column(name="name")
	public String name;
	
	@column(name="description") 
	public String description;
	
	@column(name="test_id",Index=Index.ForeignKey, AssociationType=AssociationType.HasOne)
	public TesterModel tester;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@column(name="test_id",Index=Index.ForeignKey,AssociationType=AssociationType.HasMany)
	public DevicesDataHubArrayList devices;

}
