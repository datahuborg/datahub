package DataHubORMTests;

import java.util.ArrayList;

import org.junit.Test;

import Workers.GenericCallback;

import DataHubORM.DataHubException;
import Examples.TestModel;

public class ModelBasicTestsAsync extends TestsMain{
	@Test
	public void createAndDelete() throws DataHubException, InterruptedException{
		final TestModel tm1 = newTestModel();
		tm1.saveAsync(new GenericCallback<Void>(){
			
			@Override
			public void call(Void data) throws DataHubException {
				System.out.println(tm1);
				tm1.destroyAsync(new GenericCallback<Void>(){

					@Override
					public void call(Void data) throws DataHubException {
						// TODO Auto-generated method stub
						
					}});
				
			}});
		final TestModel tm2 = newTestModel();
		tm2.saveAsync(new GenericCallback<Void>(){
			
			@Override
			public void call(Void data) throws DataHubException {
				System.out.println(tm1);
				tm2.destroyAsync(new GenericCallback<Void>(){

					@Override
					public void call(Void data) throws DataHubException {
						// TODO Auto-generated method stub
						
					}});
				
			}});
		Thread.sleep(7000);
	}
}
