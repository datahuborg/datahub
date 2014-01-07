package Examples;

import Annotations.Association;
import Annotations.Column;
import Annotations.Association.AssociationType;
import Annotations.Column.Index;
import Annotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table(name="device")
public class DeviceModel extends DataHubModel<DeviceModel>{

	public DeviceModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="code")
	public String code;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@Association(associationType = AssociationType.BelongsTo, foreignKey = "test_id")
	public TestModel testModel;
}
