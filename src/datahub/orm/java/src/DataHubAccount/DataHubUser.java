package DataHubAccount;

public class DataHubUser {

	private String username;
	private String password;
	
	public DataHubUser(String username, String password){
		this.username = username;
		this.password = password;
	}
	public String getUsername(){
		return this.username;
	}
	public String getPassword(){
		return this.password;
	}
}
