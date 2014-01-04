package Examples;

import Annotations.column;
import Annotations.table;
import DataHubORM.DataHubException;
import DataHubORM.Model;

@table(name="users")
public class UserModel extends Model<UserModel>{
	
	public UserModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@column(name="username")
	public String username;

}
