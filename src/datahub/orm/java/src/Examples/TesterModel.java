package Examples;

import Annotations.column;
import Annotations.column.Index;
import Annotations.column.AssociationType;
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
	
	@column(name="test_id",Index=Index.ForeignKey, AssociationType=AssociationType.BelongsTo)
	public TestModel test;
}
