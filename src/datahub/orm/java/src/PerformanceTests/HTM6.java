package PerformanceTests;

import DataHubAnnotations.Association;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table
public class HTM6 extends DataHubModel<HTM6>{

	public HTM6() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}
	
	@Association(associationType=AssociationTypes.BelongsTo)
	public HeavyTestModel ht;
}
