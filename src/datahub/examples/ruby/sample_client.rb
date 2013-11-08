#!/usr/bin/env ruby

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample ruby code accesing DataHub APIs
'''
$:.unshift File.dirname(__FILE__)
$:.push('gen-rb')

require 'thrift'

require 'datahub'

begin
  transport = Thrift::BufferedTransport.new(Thrift::Socket.new('datahub-experimental.csail.mit.edu', 9000))
  protocol = Thrift::BinaryProtocol.new(transport)
  client = Calculator::Client.new(protocol)

  transport.open()

  print client.version

  transport.close()

rescue Thrift::Exception => tx
  print 'Thrift::Exception: ', tx.message, "\n"
end