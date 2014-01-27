package Examples;

import DataHubAnnotations.AccessControl;
import DataHubAnnotations.AnnotationsConstants;
import DataHubAnnotations.Association;
import DataHubAnnotations.Column;
import DataHubAnnotations.Table;
import DataHubAnnotations.VarCharField;
import DataHubAnnotations.Verify;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Association.RemovalOptions;
import DataHubAnnotations.Column.Index;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Verify()
@Table(setupMode=AnnotationsConstants.SetupModes.Manual, name="device")
public class DeviceModel extends DataHubModel<DeviceModel>{

	public DeviceModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="code")
	@VarCharField(size=1000)
	public String code;
	
	//need to specify foreign key name that matches the foreign key in the corresponding belongs to relationship
	@Association(setupMode=AnnotationsConstants.SetupModes.Manual, associationType = AssociationTypes.BelongsTo, foreignKey = "test_id", removalOption=RemovalOptions.CascadingDelete)
	public TestModel testModel;
	
}
