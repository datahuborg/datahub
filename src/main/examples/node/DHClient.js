/**
@author: anant bhardwaj
@date: Oct 11, 2013

Sample nodejs code accesing DataHub APIs
*/

var http = require('http')
  thrift = require('thrift'),
  DataHub = require('DataHub.js'),
  ttypes = require('datahub_types.js');

var req = http.request("http://datahub.csail.mit.edu/service");
connection = new thrift.Connection(req);
var client = thrift.createClient(DataHub, connection);
client.get_version(function(err, version) {
  if (err) {
    console.log('DataHub error:', err);
  } else {
    console.log('DataHub version:', version);
  }
});

req.on('error', function(e) {
  console.log('problem with request: ' + e.message);
});
