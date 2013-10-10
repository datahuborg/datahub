DataHub
=======
### Dependencies
* install thrift

### Runnning DataHub Server
`cd src/datahub`

`thrift --gen py datahub.thrift`

`export PYTHONPATH=$PYTHONPATH:/path/to/datahub:/path/to/datahub/gen-py`

`python server.py`

### Running DataHub Client
`cd src/datahub`

`python client/python/dh_client.py`

### Running DataHub Interactive Shell
`cd src/datahub`

`python tools/cli.py`
