package Examples;

import DataHubORM.DataHubArrayList;
import DataHubORM.DataHubConverter;
import DataHubORM.DataHubException;

public class DevicesDataHubArrayList extends DataHubArrayList<DeviceModel>{

	public DevicesDataHubArrayList() throws DataHubException {
		super();
		// TODO Auto-generated constructor stub
	}
	//subclass of datahub arraylist required so that the generic type is not erased,
	//the generic type of the superclass is kept around for the subclass
	//Type Erasure is stupid
}
