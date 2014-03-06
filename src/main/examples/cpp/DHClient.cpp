#include <unistd.h>
#include <boost/shared_ptr.hpp>

#include "gen-cpp/DataHub.h"
#include <thrift/transport/THttpClient.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/protocol/TBinaryProtocol.h>

/**
 * Sample DataHub C++ Client
 *
 * @author anantb
 * @date 11/07/2013
 *
 */

using namespace std;
using namespace boost;
using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

using namespace datahub;

int main () {
  try {
    shared_ptr<THttpClient> http(new THttpClient("datahub.csail.mit.edu", 80, "/service"));
    shared_ptr<TBinaryProtocol> protocol(new TBinaryProtocol(http));
    DataHubClient client(protocol);

    http->open();
    double version = client.get_version();
    cout << version << endl;

    DHConnectionParams params;
    params.user = "anantb";
    params.password = "anant";

    DHConnection conn;
    client.connect(conn, params);
    cout << conn.id << endl;

    DHQueryResult res;
    client.execute_sql(res, conn, "select * from anantb.demo.team", vector<string>());

    http->close();
  } catch (TException &tx) {
    cout << "ERROR: " << tx.what();
  }

  return 0;
}
