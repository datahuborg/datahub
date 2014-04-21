package DataHubORMTests;

import java.util.ArrayList;

import org.junit.Test;


import DataHubORM.DataHubException;
import DataHubWorkers.GenericCallback;
import Examples.TestModel;
import Examples.UserModel;

public class ModelBasicTestsAsync extends TestsMain{
	@Test
	public void createAndDelete() throws DataHubException, InterruptedException{
		final TestModel tm1 = newTestModel();
		tm1.saveAsync(new GenericCallback<TestModel>(){
			
			@Override
			public void call(TestModel data){
				System.out.println(data);
				try {
					data.destroyAsync(new GenericCallback<Void>(){

						@Override
						public void call(Void data){
							// TODO Auto-generated method stub
							
						}}, new GenericCallback<DataHubException>(){

							@Override
							public void call(DataHubException data){
								// TODO Auto-generated method stub
								
						}});
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}}, new GenericCallback<DataHubException>(){

				@Override
				public void call(DataHubException data){
					// TODO Auto-generated method stub
					
		}});
		final TestModel tm2 = newTestModel();
		tm2.saveAsync(new GenericCallback<TestModel>(){
			
			@Override
			public void call(TestModel data){
				System.out.println(data);
				try {
					data.destroyAsync(new GenericCallback<Void>(){

						@Override
						public void call(Void data){
							// TODO Auto-generated method stub
							
						}}, new GenericCallback<DataHubException>(){

							@Override
							public void call(DataHubException data){
								// TODO Auto-generated method stub
								
						}});
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}}, new GenericCallback<DataHubException>(){

				@Override
				public void call(DataHubException data){
					// TODO Auto-generated method stub
					
		}});
		final TestModel tm3 = newTestModel();
		tm3.saveAsync(new GenericCallback<TestModel>(){
			
			@Override
			public void call(TestModel data){
				System.out.println(data);
				try {
					data.destroyAsync(new GenericCallback<Void>(){

						@Override
						public void call(Void data){
							// TODO Auto-generated method stub
							
						}}, new GenericCallback<DataHubException>(){

							@Override
							public void call(DataHubException data){
								// TODO Auto-generated method stub
								
						}});
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}}, new GenericCallback<DataHubException>(){

				@Override
				public void call(DataHubException data){
					// TODO Auto-generated method stub
					
		}});
		final TestModel tm4 = newTestModel();
		tm4.saveAsync(new GenericCallback<TestModel>(){
			
			@Override
			public void call(TestModel data){
				System.out.println(data);
				try {
					data.destroyAsync(new GenericCallback<Void>(){

						@Override
						public void call(Void data){
							// TODO Auto-generated method stub
							
						}}, new GenericCallback<DataHubException>(){

							@Override
							public void call(DataHubException data){
								// TODO Auto-generated method stub
								
						}});
				} catch (DataHubException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
			}}, new GenericCallback<DataHubException>(){

				@Override
				public void call(DataHubException data){
					// TODO Auto-generated method stub
					
		}});
		Thread.sleep(5000);
	}
	@Test
	public void query() throws DataHubException, InterruptedException{
		final UserModel tm4 = new UserModel();
		tm4.saveAsync(new GenericCallback<UserModel>(){

			@Override
			public void call(UserModel data){
		    	//do something with new data
		    }
		}, new GenericCallback<DataHubException>(){

				@Override
				public void call(DataHubException data){
					//handle exception if save() failed
				}
		});
	}
}
