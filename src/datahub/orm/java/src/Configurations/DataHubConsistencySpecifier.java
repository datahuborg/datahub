package Configurations;

public class DataHubConsistencySpecifier {

	public enum ConsistencyLevels{SingleCopy, DelayedWrite, WriteWhenChargingOrBeforeDisconnect};
	
	private ConsistencyLevels consistencyLevel;
	
	public DataHubConsistencySpecifier(){
		this.consistencyLevel = ConsistencyLevels.SingleCopy;
	}
	public void setConsistencyLevel(ConsistencyLevels consistencyLevel){
		this.consistencyLevel = consistencyLevel;
	}
	public ConsistencyLevels getConsistencyLevel(){
		return this.consistencyLevel;
	}
}
