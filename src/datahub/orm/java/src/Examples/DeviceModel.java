package Examples;

import Annotations.Association;
import Annotations.Column;
import Annotations.Association.AssociationTypes;
import Annotations.Column.Index;
import Annotations.Table;
import Annotations.VarCharField;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table(name="device")
public class DeviceModel extends DataHubModel<DeviceModel>{

	public DeviceModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="code")
	@VarCharField(size=20)
	public String code;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@Association(associationType = AssociationTypes.BelongsTo, foreignKey = "test_id")
	public TestModel testModel;
}
