package Examples;

import Annotations.Association;
import Annotations.Association.AssociationType;
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
	public String testerName;
	
	@Association(associationType = AssociationType.BelongsTo, foreignKey = "test_id")
	public TestModel test;
}
