package DataHubORMTests;

import Annotations.column;
import Annotations.column.Index;
import Annotations.column.RelationType;
import Annotations.table;
import DataHubORM.Model;

@table(name="device")
public class DeviceModel extends Model<DeviceModel>{

	@column(name="code")
	public String code;
	
	@column(name="test_id",RelationType=RelationType.BelongsTo)
	public TestModel testModel;
}
