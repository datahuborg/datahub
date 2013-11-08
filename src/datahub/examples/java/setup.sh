#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../../../.."; pwd)

rm -rf $abspath/bin
rm -rf $abspath/gen-java

thrift --gen java -o $abspath $basepath/src/datahub/datahub.thrift
mkdir $abspath/bin
jar=$(cd "$basepath/lib/third-party/java"; pwd)
CLASSPATH=$CLASSPATH:$jar/thrift/libthrift-0.9.1.jar:$jar/slf4j/slf4j-api-1.7.5.jar:$abspath/bin:$abspath/gen-java
export CLASSPATH
javac -classpath $CLASSPATH -d $abspath/bin $abspath/src/DHClient.java