package Examples;

import DataHubORM.DataHubArrayList;
import DataHubORM.DataHubConverter;

public class DevicesDataHubArrayList extends DataHubArrayList<DeviceModel>{
	//subclass of datahub arraylist required so that the generic type is not erased,
	//the generic type of the superclass is kept around for the subclass
	//Type Erasure is stupid
}
