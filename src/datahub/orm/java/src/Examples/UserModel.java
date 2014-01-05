package Examples;

import Annotations.association;
import Annotations.column;
import Annotations.table;
import Annotations.association.AssociationType;
import DataHubORM.DataHubException;
import DataHubORM.Model;

@table(name="users")
public class UserModel extends Model<UserModel>{
	
	public UserModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@column(name="username")
	public String username;
	
	@association(associationType = AssociationType.HasAndBelongsToMany, linkingTable = "testuser", leftTableForeignKey = "test_id",rightTableForeignKey = "user_id", foreignKey = "user_id")
	public TestDatahubArrayList tests;
}
