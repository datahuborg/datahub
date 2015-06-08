import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.THttpClient;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import java.nio.ByteBuffer;
import datahub.*;
import datahub.account.*;
import datahub.account.AccountService;

/** 
 * Sample Java Client for DataHub
 * 
 * @author al carter
 * @date 06/08/2015
 * 
 */

public class SampleAccount {
  public static void main(String [] args) {
    try {
      // This will initially thrown an exception since
      // You will need to register an application and assign
      // the variables below.
      // then, log in as the user, and visit this url to authorize the app:
      // https://datahub.csail.mit.edu/permissions/apps/allow_access/APP_ID/REPO_NAME
      // see the /developer/apps page to register an application.

      String username = "USERNAME";
      String password = "PASSWORD";
      String email = "EMAIL";
      String repo = "REPO";       // the repository that your app operates on
      String table = "TABLE"; // the table we will create
      String app_id = "APP_ID";             // your app's unique id
      String app_token = "app_token";       // your app's unique token
          

      // Before running you will need to populate the above variables
      // and create a corresponding repo and table in your datahub acount
          
      // http setup
      TTransport transport = new THttpClient("http://datahub.csail.mit.edu/service");
      TProtocol protocol = new  TBinaryProtocol(transport);
      DataHub.Client client = new DataHub.Client(protocol);;
      System.out.println("Version: " + client.get_version());

      ConnectionParams con_params = new ConnectionParams();
      // con_params.setUser(username);
      con_params.setRepo_base(username);
      con_params.setApp_id(app_id);
      con_params.setApp_token(app_token);
      // AccountService.Client client = new AccountService(con_params);

      Connection con = client.open_connection(con_params);


      System.out.println("\n\nTrying to query a user's table...");
      String query = "select * from " + username + "." + repo + "." + table;
      ResultSet res = client.execute_sql(con, query, null);

      // print field names
      for (String field_name : res.getField_names()) {
        System.out.print(field_name + "\t");
      }

      System.out.println();

      // print tuples
      for (Tuple t : res.getTuples()) {
        for (ByteBuffer cell : t.getCells()) {
          System.out.print(new String(cell.array()) + "\t");
        }
        System.out.println();
      }
 
    } catch(Exception e) {
      e.printStackTrace();
    }
  }
}
