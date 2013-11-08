#include <unistd.h>

#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>

#include "../gen-cpp/DataHub.h"

/** 
 * Sample DataHub C++ Client
 * 
 * @author anantb
 * @date 11/07/2013
 * 
 */

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace datahub;

int main () {
  try:
    shared_ptr socket(new TSocket("datahub-experimental.csail.mit.edu", 9000));
    shared_ptr transport(new TBufferedTransport(socket));
    shared_ptr protocol(new TBinaryProtocol(transport));
    DataHub client(protocol);

    transport->open();
    double version = client.get_version();
    cout << version; 

    transport->close();
  } catch (TException &tx) {
    cout << "ERROR: " << tx.what();
  }

  return 0;
}
