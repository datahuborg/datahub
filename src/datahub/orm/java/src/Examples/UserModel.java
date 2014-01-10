package Examples;

import Annotations.Association;
import Annotations.Column;
import Annotations.Table;
import Annotations.Association.AssociationType;
import Annotations.VarCharField;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table(name="users")
public class UserModel extends DataHubModel<UserModel>{
	
	public UserModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="username")
	@VarCharField(size=30)
	public String username;
	
	@Association(associationType = AssociationType.HasAndBelongsToMany, linkingTable = "testuser", leftTableForeignKey = "test_id",rightTableForeignKey = "user_id", foreignKey = "user_id")
	public TestDatahubArrayList tests;
}
