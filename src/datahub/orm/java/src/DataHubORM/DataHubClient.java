package DataHubORM;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TJSONProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.THttpClient;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

import datahub.DHCell;
import datahub.DHConnection;
import datahub.DHConnectionParams;
import datahub.DHData;
import datahub.DHException;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;
import datahub.DataHub;
import datahub.DHConnectionParams._Fields;
import datahub.DataHub.Client;

import DataHubAccount.DataHubAccount;
import DataHubResources.Constants;
import DataHubResources.Resources;

//TODO: convert all exceptions to datahub exceptions
//each user should have datahub table so that we know which databases are currently allocated to user
//actual database names should have username as prefix so unique
class DataHubClient{
	private DataHubAccount dha;
	private DataHubDatabase database;
	private boolean isDBSet;
	//possibly add support for  connection to many databases
	//arraylist of datahum  clients
	public DataHubClient(DataHubAccount dha){
		this.dha = dha;
		this.isDBSet = false;
	}

	private void checkRep() throws Exception{
	}
	private DHConnectionParams getConnectionParams(DataHubDatabase db){
		DHConnectionParams dhcp = new DHConnectionParams();
		dhcp.setFieldValue(_Fields.USER, dha.getUser().getPassword());
		dhcp.setFieldValue(_Fields.PASSWORD, dha.getApiKey());
		dhcp.setFieldValue(_Fields.REPO, db.getDatabaseName());
		return dhcp;
	}
	private synchronized Client getNewClient() throws DHException, TException{
		TTransport transport = new THttpClient("http://datahub-experimental.csail.mit.edu/service");
		//TTransport transport = new THttpClient("http://datahub.csail.mit.edu/service");
	    TProtocol protocol = new TBinaryProtocol(transport);
		Client client = new DataHub.Client(protocol);
		return client;
	}
	private synchronized DHConnection getNewConnection(Client c) throws DHException, TException{
		DHConnectionParams dhcp = getConnectionParams(database);
		return c.connect(dhcp);
	}
	public synchronized void setDatabase(DataHubDatabase db){
		database = db;
		this.isDBSet = true;
	}
	public synchronized void disconnect(){
	}
	public boolean isDBSet(){
		return this.isDBSet;
	}
	//TODO:possible security issue with unauthorized manipulation of client cause propagating changes to 
	//server that destroy database
	public synchronized void updateSchema(DataHubDatabase db) throws DHException, TException{
		detectSchemaDifferences();
	}
	public DHQueryResult getDatabaseSchema() throws DHException, TException{
		Client localClient = this.getNewClient();
		return localClient.list_tables(getNewConnection(localClient), this.database.getDatabaseName());
	}
	private void detectSchemaDifferences() throws DHException, TException{
		DHQueryResult dbSchema = getDatabaseSchema();
		DHData data = dbSchema.getData();
		DHSchema schema = data.getSchema();
		DHTable table  = data.getTable();
	}
	public DHQueryResult dbQuery(String query){
		DHQueryResult out = null;
		try{
			Client localClient = this.getNewClient();
			out = localClient.execute_sql(getNewConnection(localClient), query, null);
		}catch(Exception e){
			e.printStackTrace();
		}
		return out;
	}
}
