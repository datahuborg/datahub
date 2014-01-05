package Examples;

import Annotations.association;
import Annotations.association.AssociationType;
import Annotations.column;
import Annotations.column.Index;
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
	
	@association(associationType = AssociationType.HasOne, foreignKey = "test_id")
	public TesterModel tester;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@association(associationType = AssociationType.HasMany, foreignKey = "test_id")
	public DevicesDataHubArrayList devices;
	
	@association(associationType = AssociationType.HasAndBelongsToMany, linkingTable = "testuser", leftTableForeignKey = "test_id",rightTableForeignKey = "user_id", foreignKey = "test_id")
	public UsersDataHubArrayList users;

}
