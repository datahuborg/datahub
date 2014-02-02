package Examples;

import DataHubAnnotations.Association;
import DataHubAnnotations.Association.LoadTypes;
import DataHubAnnotations.AnnotationsConstants;
import DataHubAnnotations.Column;
import DataHubAnnotations.NoDownload;
import DataHubAnnotations.Table;
import DataHubAnnotations.VarCharField;
import DataHubAnnotations.Verify;
import DataHubAnnotations.Association.AssociationTypes;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;
import DataHubORM.QueryRefinementObject;

@Table(setupMode=AnnotationsConstants.SetupModes.Manual, name="users")
public class UserModel extends DataHubModel<UserModel>{
	
	//require constructor with no arguments to set defaults
	public UserModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column(setupMode=AnnotationsConstants.SetupModes.Manual, name="username")
	@VarCharField(size=1000)
	public String username;
	
	@Column(setupMode=AnnotationsConstants.SetupModes.Manual,name="password")
	@VarCharField(size=1000)
	public String password;
	
	@Column
	public String description;
	
	@Column
	public double funds;
	
	@Association(setupMode=AnnotationsConstants.SetupModes.Manual, associationType = AssociationTypes.HasAndBelongsToMany, linkingTable = "testuser", leftTableForeignKey = "test_id",rightTableForeignKey = "user_id", foreignKey = "user_id")
	public TestDatahubArrayList tests;
	
	@Association(associationType = AssociationTypes.HasAndBelongsToMany, loadType = LoadTypes.None)
	public CarDataHubArrayList cars;
	
	@Override
	public synchronized boolean validate(){
		return true;
	}
	
	@Override
	public synchronized void beforeSave(){

	}
	
	@Override
	public synchronized void afterSave(){
		
	}
	
	@Override
	public synchronized void beforeDestroy(){
		
	}
	
	@Override
	public synchronized void afterDestroy(){
		
	}

	//override this method to set defaults for fields in class
	@Override
	public void setDefaults(){
		this.password = "lol";
		this.description = "Enter a description here!";
		this.funds = 0;
	}
	
	//Override this method to use this default query refinment object in all queries for class
	//where query refinment object not specified
	@Override
	public QueryRefinementObject getDefaultQueryRefinemnetObject(){
		return new QueryRefinementObject();
	}
	
	
}
