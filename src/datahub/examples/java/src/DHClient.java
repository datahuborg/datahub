import datahub.*;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TSSLTransportFactory;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TSSLTransportFactory.TSSLTransportParameters;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;

public class DHClient {
  public static void main(String [] args) {
    try {
      TTransport transport = new TSocket("datahub-experimental.csail.mit.edu", 9000);
      transport.open();

      TProtocol protocol = new  TBinaryProtocol(transport);
      DataHub.Client client = new DataHub.Client(protocol);
      System.out.println(client.get_version());


      transport.close();
    } catch(Exception e) {
      e.printStackTrace();
    }

   
  }

}
