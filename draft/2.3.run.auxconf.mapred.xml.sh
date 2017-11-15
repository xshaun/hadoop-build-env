#!/bin/bash
#
source 0.*

# * Make the HDFS directories required to execute MapReduce jobs:
${HADOOP_CODE_PATH}/sbin/start-dfs.sh
${HADOOP_CODE_PATH}/bin/hdfs dfs -mkdir /user
${HADOOP_CODE_PATH}/bin/hdfs dfs -mkdir /user/root
${HADOOP_CODE_PATH}/sbin/stop-dfs.sh

# MR on yarn
#
# * etc/hadoop/mapred-site.xml
put_config_xml  \
    --file ${HADOOP_CODE_PATH}'/etc/hadoop/mapred-site.xml'   \
    --property 'mapreduce.framework.name'   \
    --value 'yarn'

# * etc/hadoop/yarn-site.xml
put_config_xml  \
    --file ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'    \
    --property 'yarn.nodemanager.aux-services'   \
    --value 'mapreduce_shuffle'

put_config_xml  \
    --file ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'    \
    --property 'yarn.nodemanager.env-whitelist'   \
    --value 'JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME'


