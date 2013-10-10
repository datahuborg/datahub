DataHub
=======
### Dependencies
* thrift
* postgres

### Runnning DataHub Server
`cd src/datahub`

`thrift --gen py datahub.thrift`

`python server.py`


### Running DataHub Interactive Shell
`cd src/datahub`

`export PYTHONPATH=$PYTHONPATH:.:./gen-py`

`python tools/cli.py`
