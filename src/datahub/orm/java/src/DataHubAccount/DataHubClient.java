package DataHubAccount;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TJSONProtocol;
import org.apache.thrift.transport.TSocket;
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

import DataHubORM.Database;
import DataHubResources.Constants;
import DataHubResources.Resources;

//TODO: convert all exceptions to datahub exceptions
//each user should have datahub table so that we know which databases are currently allocated to user
//actual database names should have username as prefix so unique
public class DataHubClient{
	private DataHubAccount dha;
	private DHConnection currentConnection;
	private Client client;
	private TSocket socket;
	private Database database;
	private boolean connectedToDB;
	//possibly add support for  connection to many databases
	//arraylist of datahum  clients
	public DataHubClient(DataHubAccount dha){
		this.dha = dha;
	}
	private void checkDBConnection() throws Exception{
		if(!connectedToDB){
			throw new Exception("Not connected to DB!");
		}
	}
	private void checkRep() throws Exception{
		if(currentConnection == null){
			throw new Exception("Connection not initialized!");
		}
	}
	private TSocket getConnectionSocket(){
		return new TSocket(Constants.SERVER_ADDR_ROOT,Constants.SERVER_ADDR_PORT);
	}
	private DHConnectionParams getConnectionParams(Database db){
		DHConnectionParams dhcp = new DHConnectionParams();
		dhcp.setFieldValue(_Fields.USER, dha.getUser().getPassword());
		dhcp.setFieldValue(_Fields.PASSWORD, dha.getApiKey());
		dhcp.setFieldValue(_Fields.REPO, db.getDatabaseName());
		return dhcp;
	}
	public void connect(Database db) throws DHException, TException{
		TSocket newSocket = getConnectionSocket();
		socket = newSocket;
		socket.open();
		TBinaryProtocol bp = new TBinaryProtocol(socket);
		//TJSONProtocol jp = new TJSONProtocol(socket);
		client = new DataHub.Client(bp);
		database = db;
		DHConnectionParams dhcp = getConnectionParams(database);
		currentConnection = client.connect(dhcp);
		connectedToDB = true;
	}
	public void disconnect(){
		if(connectedToDB){
			socket.close();
			client = null;
			currentConnection = null;
			connectedToDB = false;
		}
	}
	//TODO:possible security issue with unauthorized manipulation of client cause propagating changes to 
	//server that destroy database
	public void updateSchema(Database db) throws DHException, TException{
		detectSchemaDifferences();
	}
	public DHQueryResult getDatabaseSchema() throws DHException, TException{
		return client.list_tables(currentConnection, this.database.getDatabaseName());
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
			out = this.client.execute_sql(this.currentConnection, query, null);
		}catch(Exception e){
			e.printStackTrace();
		}
		return out;
	}
}
