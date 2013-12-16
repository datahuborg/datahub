package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;

import org.apache.thrift.TException;

import datahub.DHException;
import datahub.DHQueryResult;

import Annotations.database;
import DataHubAccount.DataHubAccount;
import DataHubAccount.DataHubClient;
import DataHubResources.Resources;

@database(name="")
public abstract class Database {

	private DataHubClient dhc;
	
	public void setDataHubAccount(DataHubAccount dha){
		this.dhc = new DataHubClient(dha);
	}
	public void connect() throws DataHubException{
		try {
			dhc.connect(this);
		} catch (Exception e){
			//fix this
			throw new DataHubException();
		}
		instantiateAndSetup();
	}
	public void disconnect(){
		dhc.disconnect();
	}
	private void instantiateAndSetup(){
		ArrayList<Field> fields = DataHubConverter.findModels(this);
		for(Field f:fields){
			Resources.setField(this,f.getName(), Resources.fieldToInstance(f));
			try{
				//TODO: somehow make this static
				((Model) f.get(this)).setDatabase(this);
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	}
	public DHQueryResult dbQuery(String query){
		return dhc.dbQuery(query);
	}
	public String getDatabaseName(){
		database d = this.getClass().getAnnotation(database.class);
		if(d != null){
			return d.name();
		}
		return null;
	}
	
}
