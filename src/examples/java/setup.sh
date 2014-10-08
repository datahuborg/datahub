#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
basepath=$(cd "$abspath/../../.."; pwd)
jar=$(cd "$abspath/lib"; pwd)

rm -rf $abspath/bin
rm -rf $abspath/gen-java
mkdir $abspath/bin

thrift --gen java -o $abspath $basepath/src/datahub.thrift

CLASSPATH=$jar/thrift/*:$jar/slf4j/*:$jar/apache-commons/*:$abspath/bin:$abspath/gen-java
export CLASSPATH

javac -classpath $CLASSPATH -d $abspath/bin $abspath/src/SampleClient.java
