package Examples;

import Annotations.Association;
import Annotations.DoubleField;
import Annotations.VarCharField;
import Annotations.Association.AssociationTypes;
import Annotations.Column;
import Annotations.Column.Index;
import Annotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table(name="tester")
public class TesterModel extends DataHubModel<TesterModel> {

	public TesterModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(name="tester_name")
	@VarCharField(size=1000)
	public String testerName;
	
	/*@Column(name="cost")
	@FloatField()
	public float cost;*/
	
	
	@Association(associationType = AssociationTypes.BelongsTo, foreignKey = "test_id")
	public TestModel test;
}
