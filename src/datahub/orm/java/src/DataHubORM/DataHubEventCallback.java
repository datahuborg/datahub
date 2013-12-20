package DataHubORM;

import java.util.ArrayList;

public interface DataHubEventCallback<T> {
	public void call(ArrayList<T> data);
}
