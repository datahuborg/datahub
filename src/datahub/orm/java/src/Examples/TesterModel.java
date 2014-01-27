package Examples;


import DataHubAnnotations.AnnotationsConstants;
import DataHubAnnotations.Association;
import DataHubAnnotations.Column;
import DataHubAnnotations.DecimalField;
import DataHubAnnotations.Table;
import DataHubAnnotations.VarCharField;
import DataHubAnnotations.Verify;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Column.Index;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;


@Verify()
@Table(setupMode=AnnotationsConstants.SetupModes.Manual, name="tester")
public class TesterModel extends DataHubModel<TesterModel> {

	public TesterModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="tester_name")
	@VarCharField(size=1000)
	public String testerName;
	
	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="cost")
	@DecimalField()
	public double cost;
	
	
	@Association(setupMode=AnnotationsConstants.SetupModes.Manual, associationType = AssociationTypes.BelongsTo, foreignKey = "test_id")
	public TestModel test;
}
