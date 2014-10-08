import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.THttpClient;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import java.nio.ByteBuffer;
import datahub.*;

/** 
 * Sample Java Client for DataHub
 * 
 * @author anantb
 * @date 11/07/2013
 * 
 */

public class SampleClient {
  public static void main(String [] args) {
    try {
      TTransport transport = new THttpClient("http://datahub.csail.mit.edu/service");
      TProtocol protocol = new  TBinaryProtocol(transport);
      DataHub.Client client = new DataHub.Client(protocol);

      System.out.println("Version: " + client.get_version());

      // open connection
      ConnectionParams con_params = new ConnectionParams();
      con_params.setUser("anantb");
      con_params.setPassword("anant");
      Connection con = client.open_connection(con_params);
	     
      // execute a query
      ResultSet res = client.execute_sql(con, "select * from anantb.test.demo", null);

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
