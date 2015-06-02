#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

rm -rf $abspath/gen-py

thrift --gen py -o $abspath $abspath/thrift/datahub.thrift
thrift --gen py -o $abspath $abspath/thrift/account.thrift

# generate C++ apis
# ( exec $abspath"/examples/cpp/setup.sh" )

# generate Go apis
# ( exec $abspath"/examples/go/setup.sh" )

# generate java apis
# ( exec $abspath"/examples/java/setup.sh" )

# generate javascript apis
# These are hosted and don't need to be generated.

# generate objective-c apis
# ( exec $abspath"/examples/objc/setup.sh" )

# generate python apis
# ( exec $abspath"/examples/python/setup.sh" )

PYTHONPATH=$abspath:$abspath/gen-py:$abspath/apps
export PYTHONPATH

echo "\n---Finished setting up some datahub apis.---\n"
echo "If you need to generate apis for C++, Go, Java, Objective-C, or Python"
echo "Open this file, uncomment the appropriate lines, and run again:"
echo "\t$ nano setup.sh"
echo "\t$ ./setup.sh"