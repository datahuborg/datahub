import datahub.*;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.THttpClient;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;

/** 
 * Sample DataHub Java Client
 * 
 * @author anantb
 * @date 11/07/2013
 * 
 */

public class DHClient {
  public static void main(String [] args) {
    try {
      TTransport transport = new THttpClient("http://datahub.csail.mit.edu/service");
      transport.open();

      TProtocol protocol = new  TBinaryProtocol(transport);
      DataHub.Client client = new DataHub.Client(protocol);

      DHConnectionParams con_params = new DHConnectionParams();
      con_params.setUser("anantb");
      con_params.setPassword("anant");
      DHConnection con = client.connect(con_params);
	     
      DHQueryResult res = client.execute_sql(con, "select * from anantb.demo.team", null);
      System.out.println(res);
	  
      transport.close();
    } catch(Exception e) {
      e.printStackTrace();
    }
 
  }

}
