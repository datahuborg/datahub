package Examples;

import DataHubAnnotations.Column;
import DataHubAnnotations.Table;
import DataHubORM.DataHubException;
import DataHubORM.DataHubModel;

@Table
public class CarModel extends DataHubModel<CarModel>{

	public CarModel() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}

	@Column
	public String model;
	
	@Column
	public String make;
}
