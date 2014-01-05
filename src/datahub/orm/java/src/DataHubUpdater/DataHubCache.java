package DataHubUpdater;

public class DataHubCache{
	//TODO: caching policies
	public enum FreshnessLevels {Fresh,CycleRefresh, ManualRefresh}
	
	private FreshnessLevels freshnessLevel;
	
	private int refreshInterval;
	
	public void setFreshnessLevel(FreshnessLevels f){
		this.freshnessLevel = f;
	}
	public FreshnessLevels getFreshnessLevel(){
		return this.freshnessLevel;
	}
	public void setRefreshInterval(int refreshInterval){
		this.refreshInterval = refreshInterval;
	}
	public int getRefreshInterval(){
		return this.refreshInterval;
	}
}
