package Examples;


import DataHubAnnotations.Association;
import DataHubAnnotations.Column;
import DataHubAnnotations.DoubleField;
import DataHubAnnotations.Table;
import DataHubAnnotations.VarCharField;
import DataHubAnnotations.Verify;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Column.Index;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;


@Verify()
@Table(name="tester")
public class TesterModel extends DataHubModel<TesterModel> {

	public TesterModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="tester_name")
	@VarCharField(size=1000)
	public String testerName;
	
	@Column(name="cost")
	@DoubleField()
	public double cost;
	
	
	@Association(associationType = AssociationTypes.BelongsTo, foreignKey = "test_id")
	public TestModel test;
}
