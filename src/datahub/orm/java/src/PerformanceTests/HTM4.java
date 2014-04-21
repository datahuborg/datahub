package PerformanceTests;

import DataHubAnnotations.Association;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table
public class HTM4 extends DataHubModel<HTM4>{

	public HTM4() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}
	
	@Association(associationType=AssociationTypes.BelongsTo)
	public HeavyTestModel ht;
}
