package Examples;

import Annotations.column;
import Annotations.column.Index;
import Annotations.column.AssociationType;
import Annotations.table;
import DataHubORM.Model;

@table(name="tester")
public class TesterModel extends Model<TesterModel> {

	@column(name="tester_name")
	public String testerName;
	
	@column(name="test_id",Index=Index.ForeignKey, RelationType=AssociationType.BelongsTo)
	public TestModel test;
}
