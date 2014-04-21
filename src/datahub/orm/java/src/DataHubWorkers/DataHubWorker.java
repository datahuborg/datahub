package DataHubWorkers;

import java.util.concurrent.ExecutionException;

import javax.swing.SwingWorker;

import android.os.AsyncTask;

import DataHubORM.DataHubException;

public class DataHubWorker<T>{

	public static enum DataHubWorkerMode{Android, Normal};
	
	private final DataHubWorkerMode mode;
	
	private final GenericCallback<T> succeedCallback;
	
	private final GenericCallback<DataHubException> failCallback;
	
	private final GenericExecutable<T> functionToExecute;
	
	public DataHubWorker(GenericExecutable<T> functionToExecute, GenericCallback<T> succeedCallback,GenericCallback<DataHubException> failCallback,DataHubWorkerMode mode){
		this.succeedCallback = succeedCallback;
		this.failCallback = failCallback;
		this.functionToExecute = functionToExecute;
		this.mode = mode;
	}
	public DataHubWorker(GenericExecutable<T> functionToExecute, GenericCallback<T> succeedCallback,GenericCallback<DataHubException> failCallback){
		this.succeedCallback = succeedCallback;
		this.failCallback = failCallback;
		this.functionToExecute = functionToExecute;
		this.mode = DataHubWorkerMode.Normal;
	}
	public void execute() throws DataHubException{
		switch(mode){
			case Normal:
				SwingWorker<T,Void> worker = new SwingWorker<T,Void>(){

					private boolean succeed = false;
					
					private DataHubException failureException;
					
					@Override
					protected T doInBackground() throws Exception {
						try{
							T result = functionToExecute.call();
							succeed = true;
							return result;
						}catch(DataHubException e){
							succeed = false;
							failureException = e;
						}
						return null;
					}
					@Override
					public void done(){
						try{
							if(succeed){
								succeedCallback.call(get());
							}else{
								failCallback.call(failureException);
							}
						}catch(Exception e){
							//do something else here
							e.printStackTrace();
						}
					}};
					worker.execute();
				break;
			case Android:
				AsyncTask<Void,Void,T> androidWorker = new AsyncTask<Void,Void,T>(){

					private boolean succeed = false;
					
					private DataHubException failureException;
					
					@Override
					protected T doInBackground(Void... params){
						// TODO Auto-generated method stub
						try {
							T result = functionToExecute.call();
							succeed = true;
							return result;
						} catch (DataHubException e) {
							// TODO Auto-generated catch block
							succeed = false;
							failureException = e;
						}
						return null;
					}
					@Override
					protected void onPostExecute(T result){
						if(succeed){
							succeedCallback.call(result);
						}else{
							failCallback.call(failureException);
						}
					}};
					androidWorker.execute();
				break;
			default:
				throw new DataHubException("Invalid DataHubWorker mode!");
		}
	}

}
