#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../../../.."; pwd)

rm -rf $abspath/bin
rm -rf $abspath/gen-java

thrift --gen java -o $abspath $basepath/src/datahub/datahub.thrift
mkdir $abspath/bin
jar=$(cd "$abspath/lib"; pwd)
CLASSPATH=$CLASSPATH:$jar/thrift/*:$jar/slf4j/*:$abspath/bin:$abspath/gen-java
export CLASSPATH
javac -classpath $CLASSPATH -d $abspath/bin $abspath/src/DHClient.java