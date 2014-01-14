package DataHubORM;

public class QueryRefinementObject {
	private String orderBy;
	private String groupBy;
	private String[] distinct;
	private int querySizeLimit;
	
	public void setOrderByField(String fieldName){
		this.orderBy = fieldName;
	}
	public void setGroupByField(String fieldName){
		this.groupBy = fieldName;
	}
	public void setDistinctFieldNames(String[] distinctFieldNames){
		this.distinct = distinctFieldNames;
	}
	public void setQueryLimitSize(int sizeLimit){
		this.querySizeLimit = sizeLimit;
	}
	public String getOrderByField(){
		return this.orderBy;
	}
	public String getGroupByField(){
		return this.groupBy;
	}
	public String[]  getDistinctFieldNames(){
		return this.distinct;
	}
	public int getQuerySizeLimit(){
		return this.querySizeLimit;
	}
}
