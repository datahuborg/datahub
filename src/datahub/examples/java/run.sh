#!/bin/sh
abspath=$(cd "$(dirname "$0")"; pwd)
rm -rf $abspath/bin
rm -rf $abspath/gen-java
thrift --gen java -o $abspath $abspath/../../datahub.thrift
mkdir $abspath/bin
CLASSPATH=$CLASSPATH:$abspath/lib/*:$abspath/bin:$abspath/gen-java
javac -classpath $CLASSPATH -d $abspath/bin $abspath/src/DHClient.java
export CLASSPATH
java -classpath $CLASSPATH DHClient