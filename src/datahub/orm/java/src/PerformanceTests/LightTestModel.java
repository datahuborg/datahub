package PerformanceTests;

import DataHubAnnotations.Column;
import DataHubAnnotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table
public class LightTestModel extends DataHubModel<LightTestModel>{

	public LightTestModel() throws DataHubException {
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

}
