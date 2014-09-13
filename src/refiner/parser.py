import tokenize, token

'''
@author: anant bhardwaj
@date: May 6, 2014

parse a given text and return lexical tokens
'''

def parse(text):
  token_generator = tokenize.generate_tokens(iter([text]).next)   # tokenize the string
  chunks = [(token.tok_name[t[0]], t[1]) for t in token_generator]
  return chunks

if __name__ == "__main__":
  text = [
  "2012-01-04 00:01:23,180 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Receiving block blk_-2281137920769708011_1116 src: /127.0.0.1:32981 dest: /127.0.0.1:50010",
  "2012-01-04 00:01:23,184 INFO org.apache.hadoop.hdfs.server.datanode.DataNode.clienttrace: src: /127.0.0.1:32981, dest: /127.0.0.1:50010, bytes: 3758, op: HDFS_WRITE, cliID: DFSClient_-603743753, offset: 0, srvID: DS-292194659-127.0.1.1-50010-1324763300176, blockid: blk_-2281137920769708011_1116, duration: 2016056",
  "2012-01-04 00:01:23,185 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: PacketResponder 0 for block blk_-2281137920769708011_1116 terminating",
  "2012-01-04 00:01:23,291 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Receiving block blk_3766031435252346505_1117 src: /127.0.0.1:32982 dest: /127.0.0.1:50010",
  "2012-01-04 00:01:23,293 INFO org.apache.hadoop.hdfs.server.datanode.DataNode.clienttrace: src: /127.0.0.1:32982, dest: /127.0.0.1:50010, bytes: 265, op: HDFS_WRITE, cliID: DFSClient_-603743753, offset: 0, srvID: DS-292194659-127.0.1.1-50010-1324763300176, blockid: blk_3766031435252346505_1117, duration: 552828",
  "2012-01-04 00:01:23,293 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: PacketResponder 0 for block blk_3766031435252346505_1117 terminating",
  "2012-01-04 00:01:23,324 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Receiving block blk_-8044922265890142318_1118 src: /127.0.0.1:32983 dest: /127.0.0.1:50010"]
  for line in text:
    chunks = parse(line)
    print chunks