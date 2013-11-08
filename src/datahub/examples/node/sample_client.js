/**
@author: anant bhardwaj
@date: Oct 11, 2013

Sample javascript code accesing DataHub APIs
*/

var thrift = require('thrift'),
  DataHub = require('./gen-nodejs/DataHub.js'),
  ttypes = require('./gen-nodejs/datahub_types.js'),
  connection = thrift.createConnection(
    'datahub-experimental.csail.mit.edu',
    9000, {
    transport: thrift.TBufferedTransport,
    protocol: thrift.TBinaryProtocol
  });

connection.on('connect', function() {
  var client = thrift.createClient(DataHub, connection);
  client.get_version(function(err, version) {
    if (err) {
      console.log('DataHub error:', err);
    } else {
      console.log('DataHub version:', version);
    }
    connection.end();
  });
});

connection.on('error', function(err){
  console.log('error', err);
});