### C++ Sample Code
* `cd cpp`
* `source setup.sh`
* `./SampleClient`

### Java Sample Code
* `cd java`
* `source setup.sh`
* `java SampleClient`
* `java SampleAccount` (Non-functioning as of 2015-03-29ls
 due to thrift issues.)

### Python Sample Code
* `cd python`
* `source setup.sh`
* `mv gen-py gen_py`
* `python SampleClient.py`
* `python SampleAccount.py` (Non-functioning as of 2015-03-29 due to thrift issues.)

### Go Sample Code
* `cd go`
* `source setup.sh`
* `go run SampleClient.go`

### JavaScript Sample Code
* `cd javascript`
* open `SampleClient.html` in a browser

### Objective-C Sample Code
* `cd objc`
* `open DataHub-Example`
* run
* When integrating thrift, in Build Settings:
 * Always Search User Path: `YES`
 * Framework Search Paths: add `$(SRCROOT)`
