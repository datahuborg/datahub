package DataHubWorkers;

import DataHubORM.DataHubException;

public interface GenericExecutable<T> {

	public T call() throws DataHubException;
}
