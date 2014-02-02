package Examples;

import java.util.Date;

import DataHubAnnotations.AnnotationsConstants;
import DataHubAnnotations.Association;
import DataHubAnnotations.BooleanField;
import DataHubAnnotations.CharField;
import DataHubAnnotations.Column;
import DataHubAnnotations.DateTimeField;
import DataHubAnnotations.Table;
import DataHubAnnotations.VarCharField;
import DataHubAnnotations.Verify;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Association.RemovalOptions;
import DataHubAnnotations.Column.Index;
import DataHubORM.DataHubArrayList;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Verify()
@Table(setupMode=AnnotationsConstants.SetupModes.Manual, name="test")
public class TestModel extends DataHubModel<TestModel> {
	
	public TestModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="name")
	@VarCharField(size=1000)
	public String name;
	
	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="description") 
	@VarCharField(size=1000)
	public String description;

	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="is_cool")
	@BooleanField()
	public boolean isCool;
	
	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="created_at")
	@DateTimeField()
	public Date createdAt;

	@Column
	public int cost;
	
	@Association(setupMode=AnnotationsConstants.SetupModes.Manual, associationType = AssociationTypes.HasOne, foreignKey = "test_id")
	public TesterModel tester;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@Association(setupMode=AnnotationsConstants.SetupModes.Manual, associationType = AssociationTypes.HasMany, foreignKey = "test_id")
	public DevicesDataHubArrayList devices;
	
	@Association(setupMode=AnnotationsConstants.SetupModes.Manual, removalOption=RemovalOptions.CascadingDelete, associationType = AssociationTypes.HasAndBelongsToMany, linkingTable = "testuser", leftTableForeignKey = "test_id",rightTableForeignKey = "user_id", foreignKey = "test_id")
	public UsersDataHubArrayList users;
	
	@Association(associationType = AssociationTypes.HasAndBelongsToMany)
	public CarDataHubArrayList cars;

}
