

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample javascript code accesing DataHub APIs
'''


var transport = new Thrift.Transport("/thrift/service/tutorial/");
var protocol  = new Thrift.Protocol(transport);
var client    = new CalculatorClient(protocol);

var version = client.get_version()
console.log(version);

