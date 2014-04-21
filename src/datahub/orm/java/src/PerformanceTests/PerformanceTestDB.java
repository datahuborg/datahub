package PerformanceTests;

import DataHubAnnotations.Database;
import DataHubORM.DataHubDatabase;
import DataHubORM.DataHubException;

@Database()
public class PerformanceTestDB extends DataHubDatabase{

	public PerformanceTestDB() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}
	
	public LightTestModel LightTestModel;
	
	public HeavyTestModel HeavyTestModel;
	
	public HTM1 htm1;
	
	public HTM2 htm2;
	
	public HTM3 htm3;
	
	public HTM4 htm4;
	
	public HTM5 htm5;
	
	public HTM6 htm6;
	
	public HTM7 htm7;
	
	public HTM8 htm8;
	
	public HTM9 htm9;
	
	public HTM10 htm10;
}
