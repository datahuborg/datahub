import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.THttpClient;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import datahub.*;

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
      TProtocol protocol = new  TBinaryProtocol(transport);
      DataHub.Client client = new DataHub.Client(protocol);

      System.out.println(client.get_version());

      DHConnectionParams con_params = new DHConnectionParams();
      con_params.setUser("anantb");
      con_params.setPassword("anant");
      DHConnection con = client.connect(con_params);
	     
      DHQueryResult res = client.execute_sql(con, "select * from anantb.test.logs", null);

      for (DHRow row : res.getData().getTable().getRows()) {
        for (DHCell cell : row.getCells()) {
          if (cell.getValue()!= null) {
            System.out.print(new String(cell.getValue()));            
          } else {
            System.out.print(cell.getValue());
          }
          System.out.print("\t");
        }
        System.out.println();
      }
      
	  
    } catch(Exception e) {
      e.printStackTrace();
    }
 
  }

}
