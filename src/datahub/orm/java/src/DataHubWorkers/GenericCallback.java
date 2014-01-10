package DataHubWorkers;

import DataHubORM.DataHubException;

public interface GenericCallback<T> {

	public void call(T data) throws DataHubException;
}
