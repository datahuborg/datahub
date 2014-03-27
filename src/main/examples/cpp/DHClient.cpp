#include <unistd.h>
#include <cassert>
#include <boost/shared_ptr.hpp>

#include "gen-cpp/DataHub.h"
#include <thrift/transport/THttpClient.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/protocol/TBinaryProtocol.h>

/**
 * Sample DataHub C++ Client
 *
 * @author anantb
 * @author stephentu
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
    shared_ptr<THttpClient> transport(new THttpClient("datahub.csail.mit.edu", 80, "/service"));
    shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
    DataHubClient client(protocol);

    transport->open();
    double version = client.get_version();
    cout << version << endl;

    DHConnectionParams params = DHConnectionParams();
    params.__set_user("anantb");
    params.__set_password("anant");

    DHConnection conn;
    client.connect(conn, params);

    DHQueryResult res;
    client.execute_sql(res, conn, "select * from anantb.demo.team", vector<string>());
    for(vector<DHRow>::iterator row_it = res.data.table.rows.begin(); row_it != res.data.table.rows.end(); ++row_it) {
      for(vector<DHCell>::iterator cell_it = (*row_it).cells.begin(); cell_it != (*row_it).cells.end(); ++cell_it) {
    	cout << (*cell_it).value << "\t";
      }
      cout << "\n";
    }

    transport->close();
  } catch (TException &tx) {
    cout << "ERROR: " << tx.what();
  }

  return 0;
}
