package DataHubAccount;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
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
public class DataHubClient {
	private DataHubAccount dha;
	private DHConnection currentConnection;
	private Client client;
	private TSocket socket;
	private Database database;
	private boolean connectedToDB = false;
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
	private DHConnectionParams getConnectionParams(){
		DHConnectionParams dhcp = new DHConnectionParams();
		dhcp.setFieldValue(_Fields.USER, dha.getUser().getPassword());
		dhcp.setFieldValue(_Fields.PASSWORD, dha.getApiKey());
		return dhcp;
	}
	public void connect() throws DHException, TException{
		TSocket newSocket = getConnectionSocket();
		socket = newSocket;
		socket.open();
		TBinaryProtocol bp = new TBinaryProtocol(socket);
		DHConnectionParams dhcp = getConnectionParams();
		client = new DataHub.Client(bp);
		currentConnection = client.connect(dhcp);
		connectedToDB = false;
	}
	public void connectToDatabase(Database database) throws Exception{
		//fix server spec so list database only returns databases allocated to specific user
		if(databaseExists(database)){
			DHConnection connection = client.connect(getConnectionParams());
			connection.validate();
			currentConnection = connection;
			connectedToDB = true;
			this.database = database;
		}else{
			throw new Exception("Database does not exist!");
		}
	}
	public void disconnect(){
		socket.close();
		client = null;
		currentConnection = null;
		connectedToDB = false;
	}
	public Boolean databaseExists(Database database) throws DHException, TException{
		//String query = "select datname from datahub where datname = "+database.getDatabaseName();
		//TODO: replace with SQL query to server to check for DB so there is no need to send
		//all databases to the client
		DHQueryResult dhqr = client.list_repos(currentConnection);
		DHData data = dhqr.data;
		DHTable table = data.table;
		DHSchema schema = data.schema;
		List<DHField> fields = schema.fields;
		List<DHRow> rows = table.rows;
		int nameInd = 0;
		for(int i = 0; i < fields.size(); i++){
			DHField field = fields.get(i);
			if(field.getName() == Constants.SERVER_DB_CHECK_FIELD_NAME){
				nameInd =  i;
				break;
			}
		}
		for(DHRow row:rows){
			DHCell cell = row.cells.get(nameInd);
			String db_name = new String(cell.getValue());
			if(db_name.equals(database.getDatabaseName())){
				return true;
			}
		}
		return false;
	}
	public void createDatabase(Database db) throws Exception{
		String query = "create schema "+Resources.sqlEscape(db.getDatabaseName());
		if(!databaseExists(db)){
			try{
				client.execute_sql(this.currentConnection, query, null);
			}catch(Exception e){
				throw new Exception("Could not create database! Error: "+e.getMessage());
			}
		}else{
			throw new Exception("Database already exists!");
		}
	}
	public void dropDatabase(Database db) throws Exception{
		String query = "drop schema "+Resources.sqlEscape(db.getDatabaseName());
		if(databaseExists(db)){
			try{
				client.execute_sql(this.currentConnection, query, null);
			}catch(Exception e){
				throw new Exception("Could not create database! Error: "+e.getMessage());
			}
		}else{
			throw new Exception("Database does not exist!");
		}
	}
	//TODO:possible security issue with unauthorized manipulation of client cause propagating changes to 
	//server that destroy database
	public void updateSchema(Database db) throws DHException, TException{
		detectSchemaDifferences(db);
	}
	private DHQueryResult getDatabaseSchema(Database db) throws DHException, TException{
		DHConnection dhc = client.connect(getConnectionParams());
		return client.list_tables(dhc, db.getDatabaseName());
	}
	private void detectSchemaDifferences(Database db) throws DHException, TException{
		DHQueryResult dbSchema = getDatabaseSchema(db);
		//need to verify names of tables
		//need to verify names of columns and column data types
		Field[] fields = db.getClass().getFields();
		for(Field f:fields){

		}
	}
}
