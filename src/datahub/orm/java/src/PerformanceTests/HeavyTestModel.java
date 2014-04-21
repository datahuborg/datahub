package PerformanceTests;

import DataHubAnnotations.Association;
import DataHubAnnotations.Column;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubAnnotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table
public class HeavyTestModel extends DataHubModel<HeavyTestModel>{

	public HeavyTestModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}
	@Column
	public String ltm1;
	
	@Column
	public int ltm2;
	
	@Column
	public double ltm3;
	
	@Column
	public float ltm4;
	
	@Column
	public String ltm5;
	
	@Column
	public String ltm6;
	
	@Column
	public int ltm7;
	
	@Column
	public boolean ltm8;
	
	@Column
	public double ltm9;
	
	@Column
	public boolean ltm10;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM1DataHubArrayList htm1s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM2DataHubArrayList htm2s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM3DataHubArrayList htm3s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM4DataHubArrayList htm4s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM5DataHubArrayList htm5s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM6DataHubArrayList htm6s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM7DataHubArrayList htm7s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM8DataHubArrayList htm8s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM9DataHubArrayList htm9s;
	
	@Association(associationType=AssociationTypes.HasMany)
	public HTM10DataHubArrayList htm10s;
}
