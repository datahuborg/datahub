package Examples;

import java.util.Date;

import Annotations.Association;
import Annotations.BooleanField;
import Annotations.CharField;
import Annotations.DateTimeField;
import Annotations.Association.AssociationTypes;
import Annotations.Column;
import Annotations.Column.Index;
import Annotations.Table;
import Annotations.VarCharField;
import DataHubORM.DataHubArrayList;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table(name="test")
public class TestModel extends DataHubModel<TestModel> {
	
	public TestModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="name")
	@VarCharField(size=1000)
	public String name;
	
	@Column(name="description") 
	@VarCharField(size=1000)
	public String description;

	@Column(name="is_cool")
	@BooleanField()
	public boolean isCool;
	
	@Column(name="created_at")
	@DateTimeField()
	public Date createdAt;

	@Association(associationType = AssociationTypes.HasOne, foreignKey = "test_id")
	public TesterModel tester;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@Association(associationType = AssociationTypes.HasMany, foreignKey = "test_id")
	public DevicesDataHubArrayList devices;
	
	@Association(associationType = AssociationTypes.HasAndBelongsToMany, linkingTable = "testuser", leftTableForeignKey = "test_id",rightTableForeignKey = "user_id", foreignKey = "test_id")
	public UsersDataHubArrayList users;

}
