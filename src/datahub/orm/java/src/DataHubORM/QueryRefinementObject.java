package DataHubORM;

public class QueryRefinementObject {
	public enum OrderByType {Ascending, Descending}
	private String orderBy;
	private OrderByType orderByType;
	private String groupBy;
	private String[] distinct;
	private int querySizeLimit;
	
	public void setOrderByField(String fieldName, OrderByType orderByType){
		this.orderBy = fieldName;
		this.orderByType = orderByType;
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
	public OrderByType getOrderByType(){
		return this.orderByType;
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
