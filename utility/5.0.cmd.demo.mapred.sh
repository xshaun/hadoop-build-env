#!/bin/bash
#
source 0.*

# The hadoop daemon log output is written to the $HADOOP_LOG_DIR directory (defaults to $HADOOP_HOME/logs).
#${HADOOP_CODE_PATH}/sbin/start-dfs.sh
#
# Browse the web interface for the NameNode; by default it is available at:
# * NameNode - http://localhost:9870/

# Start ResourceManager daemon and NodeManager daemon:
#${HADOOP_CODE_PATH}/sbin/start-yarn.sh
#
# Browse the web interface for the ResourceManager; by default it is available at:
# * ResourceManager - http://localhost:8088/

${HADOOP_CODE_PATH}/sbin/start-all.sh
sleep 30s # wait

# Run a MapReduce job.
${HADOOP_CODE_PATH}/bin/hadoop jar ${HADOOP_CODE_PATH}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-alpha2.jar pi 2 5

sleep 15s
${HADOOP_CODE_PATH}/bin/hadoop jar ${HADOOP_CODE_PATH}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.0.0-alpha2.jar pi -Dmapreduce.job.num-opportunistic-maps-percent="40" 50 100

# When you’re done, stop the daemons with:
sleep 10s
${HADOOP_CODE_PATH}/sbin/stop-all.sh
