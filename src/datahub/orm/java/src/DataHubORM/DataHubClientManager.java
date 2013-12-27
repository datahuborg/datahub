package DataHubORM;

import java.util.List;

import org.apache.thrift.TException;

import datahub.DHCell;
import datahub.DHData;
import datahub.DHException;
import datahub.DHField;
import datahub.DHQueryResult;
import datahub.DHRow;
import datahub.DHSchema;
import datahub.DHTable;
import DataHubResources.Constants;
import DataHubResources.Resources;

public class DataHubClientManager {

	/*public void createDatabase(Database db) throws Exception{
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
	}}
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
	}*/

}
