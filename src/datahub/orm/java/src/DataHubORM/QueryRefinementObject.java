package DataHubORM;

public class QueryRefinementObject {
	
	public static class OrderBy{
		public enum OrderByType {Ascending, Descending}
		private OrderByType orderByType;
		private String orderByField;
		
		public OrderBy(String orderByField, OrderByType orderByType){
			this.orderByField = orderByField;
			this.orderByType = orderByType;
		}
		public OrderByType getOrderByType(){
			return this.orderByType;
		}
		public String getOrderByField(){
			return this.orderByField;
		}
		
	}
	private OrderBy[] orderBy;
	private String[] groupBy;
	private String[] distinct;
	private int querySizeLimit;
	
	public void setOrderByFields(OrderBy[] orderBy){
		this.orderBy = orderBy;
	}
	public void setGroupByField(String[] fieldNames){
		this.groupBy = fieldNames;
	}
	public void setDistinctFieldNames(String[] distinctFieldNames){
		this.distinct = distinctFieldNames;
	}
	public void setQueryLimitSize(int sizeLimit){
		this.querySizeLimit = sizeLimit;
	}
	public OrderBy[] getOrderByFields(){
		return this.orderBy;
	}
	public String[] getGroupByFields(){
		return this.groupBy;
	}
	public String[]  getDistinctFieldNames(){
		return this.distinct;
	}
	public int getQuerySizeLimit(){
		return this.querySizeLimit;
	}
}
