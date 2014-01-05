package Examples;

import Annotations.association;
import Annotations.association.AssociationType;
import Annotations.column;
import Annotations.column.Index;
import Annotations.table;
import DataHubORM.DataHubException;
import DataHubORM.Model;

@table(name="tester")
public class TesterModel extends Model<TesterModel> {

	public TesterModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@column(name="tester_name")
	public String testerName;
	
	@association(associationType = AssociationType.BelongsTo, foreignKey = "test_id")
	public TestModel test;
}
