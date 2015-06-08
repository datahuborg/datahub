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
 * @author anantb
 * @date 11/07/2013
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

      String username = "foo_bar";
      String password = "foo_bar";
      String email = "albert.r.carter.foo_bar@gmail.com";
      String repo = "demo";       // the repository that your app operates on
      String table = "table"; // the table we will create
      String app_id = "test_id";             // your app's unique id
      String app_token = "e7633b8e-be1a-4bfa-9d02-b0611edfdfb3";       // your app's unique token
          

      // Before running you will need to populate the above variables
      // and create a corresponding repo and table in your datahub acount
          
      // http setup
      TTransport transport = new THttpClient("http://datahub.csail.mit.edu/service");
      TProtocol protocol = new  TBinaryProtocol(transport);
      AccountService.Client client = new AccountService.Client(protocol);
      System.out.println("Version: " + client.get_version());

      ConnectionParams con_params = new ConnectionParams();
      con_params.setUser(username);
      con_params.setApp_id(app_id);
      con_params.setApp_token(app_token);
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
