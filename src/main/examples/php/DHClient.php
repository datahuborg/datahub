<?php
#
# author: anant bhardwaj
# date: Oct 11, 2013
# Sample PHP code accesing DataHub APIs
#

try {
  $socket = new TSocket('datahub-experimental.csail.mit.edu', 9000);
  $transport = new TBufferedTransport($socket, 1024, 1024);
  $protocol = new TBinaryProtocol($transport);
  $client = new \datahub\DataHubClient($protocol);

  $transport->open();

  $version = $client->get_version();
  print $version;

} catch (TException $tx) {
  print 'TException: '.$tx->getMessage()."\n";
}

?>