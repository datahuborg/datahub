package Workers;

import java.util.concurrent.ExecutionException;

import javax.swing.SwingWorker;

import DataHubORM.DataHubException;

public class DataHubWorker<T>{

	public enum DataHubWorkerMode{Android, Normal};
	
	private final DataHubWorkerMode mode;
	
	private final GenericCallback<T> callback;
	
	private final GenericExecutable<T> functionToExecute;
	
	public DataHubWorker(GenericExecutable<T> functionToExecute, GenericCallback<T> callback,DataHubWorkerMode mode){
		this.callback = callback;
		this.functionToExecute = functionToExecute;
		this.mode = mode;
	}
	public DataHubWorker(GenericExecutable<T> functionToExecute, GenericCallback<T> callback){
		this.callback = callback;
		this.functionToExecute = functionToExecute;
		this.mode = DataHubWorkerMode.Normal;
	}
	public void execute() throws DataHubException{
		switch(mode){
			case Normal:
				SwingWorker<T,Void> worker = new SwingWorker<T,Void>(){

					@Override
					protected T doInBackground() throws Exception {
						return functionToExecute.call();
					}
					@Override
					public void done(){
						try{
							callback.call(get());
						}catch(Exception e){
							//do something else here
							e.printStackTrace();
						}
					}};
					worker.execute();
				break;
			case Android:
				break;
			default:
				throw new DataHubException("Invalid DataHubWorker mode!");
		}
	}

}
