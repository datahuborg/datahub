#!/bin/sh
abspath=$(cd "$(dirname "$0")"; pwd)
rm -rf $abspath/bin
rm -rf $abspath/gen-java
thrift --gen java -o $abspath $abspath/../../datahub.thrift
mkdir $abspath/bin
jar=$abspath/../../../third-party/jar
CLASSPATH=$CLASSPATH:$jar/thrift/libthrift-0.9.1.jar:$jar/slf4j/slf4j-api-1.7.5.jar:$abspath/bin:$abspath/gen-java
javac -classpath $CLASSPATH -d $abspath/bin $abspath/src/DHClient.java
export CLASSPATH
java -classpath $CLASSPATH DHClient