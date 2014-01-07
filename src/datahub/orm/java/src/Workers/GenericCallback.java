package Workers;

import DataHubORM.DataHubException;

public abstract class GenericCallback<T> {

	public abstract void call(T data) throws DataHubException;
}
