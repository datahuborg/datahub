package DataHubORMTests;

import Annotations.column;
import Annotations.table;
import DataHubORM.Model;

@table(name="users")
public class UserModel extends Model<UserModel>{
	
	@column(name="username")
	public String username;

}
