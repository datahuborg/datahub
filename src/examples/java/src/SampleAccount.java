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
      // see the /developer/apps page to register an application.

      String username = "dvoiewrtlkjsd";
      String password = "dvoiewrtlkjsd";
      String email = "dvoiewrtlkjsd@sharklasers.com";
      String repo = "repo";       // the repository that your app operates on
      String table = "table"; // the table we will create
      String app_id = "csail_livinglab_getfit_app_id";             // your app's unique id
      String app_token = "67ca5c9d-1f0b-4ecd-81cd-941d2c8b8d6a";       // your app's unique token
          

      // Before running you will need to populate the above variables
      // and create a corresponding repo and table in your datahub acount
          
      // http setup
      TTransport transport = new THttpClient("http://datahub.csail.mit.edu/service");
      TProtocol protocol = new  TBinaryProtocol(transport);
      AccountService.Client client = new AccountService.Client(protocol);
      System.out.println("Version: " + client.get_version());
      
      System.out.println("\n\nTrying to create and delete an account...");
      boolean created = client.create_account("bunnicula_dkno", table , password, repo, app_id, app_token);
      boolean deleted = client.remove_account("bunnicula_dkno", app_id, app_token);
      
      System.out.println("Account Created: ");
      System.out.println(created);
      
      System.out.println("Account Delete: ");
      System.out.println(deleted);
 
    } catch(Exception e) {
      e.printStackTrace();
    }
  }
}
