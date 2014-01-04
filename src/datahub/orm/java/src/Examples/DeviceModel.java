package Examples;

import Annotations.association;
import Annotations.column;
import Annotations.association.AssociationType;
import Annotations.column.Index;
import Annotations.table;
import DataHubORM.DataHubException;
import DataHubORM.Model;

@table(name="device")
public class DeviceModel extends Model<DeviceModel>{

	public DeviceModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@column(name="code")
	public String code;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@association(associationType = AssociationType.BelongsTo, table1ForeignKey = "test_id")
	public TestModel testModel;
}
