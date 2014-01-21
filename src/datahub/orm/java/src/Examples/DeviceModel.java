package Examples;

import Annotations.Association;
import Annotations.Association.RemovalOptions;
import Annotations.Column;
import Annotations.Association.AssociationTypes;
import Annotations.Column.Index;
import Annotations.AccessControl;
import Annotations.Table;
import Annotations.VarCharField;
import Annotations.Verify;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Verify()
@Table(name="device")
public class DeviceModel extends DataHubModel<DeviceModel>{

	public DeviceModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="code")
	@VarCharField(size=1000)
	public String code;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@Association(associationType = AssociationTypes.BelongsTo, foreignKey = "test_id", removalOption=RemovalOptions.CascadingDelete)
	public TestModel testModel;
	
	@AccessControl()
	@Association(associationType = AssociationTypes.HasMany, foreignKey = "user_id", removalOption=RemovalOptions.CascadingDelete)
	public UsersDataHubArrayList users;
}
