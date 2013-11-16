package DataHubAccount;

public class DataHubAccount {
	
	private DataHubUser user;
	private String apiKey;
	
	public DataHubAccount(String apiKey, DataHubUser user){
		this.user = user;
		this.apiKey = apiKey;
	}
	public DataHubUser getUser(){
		return this.user;
	}
	public String getApiKey(){
		return this.apiKey;
	}
	public void setDataHubUser(DataHubUser user){
		this.user = user;
	}
	public void setApiKey(String apiKey){
		this.apiKey = apiKey;
	}
}
