#!/bin/bash
#
source 0.*

_XML_FILE_HEADER='<?xml version="1.0" encoding="UTF-8"?>'"\n"'<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>'

# * Make the HDFS directories required to execute MapReduce jobs:
${HADOOP_CODE_PATH}/sbin/start-dfs.sh
${HADOOP_CODE_PATH}/bin/hdfs dfs -mkdir /yarn/user
${HADOOP_CODE_PATH}/bin/hdfs dfs -mkdir /yarn/user/root
${HADOOP_CODE_PATH}/sbin/stop-dfs.sh

# MR on yarn
#
# * etc/hadoop/mapred-site.xml
echo -e "\
${_XML_FILE_HEADER}
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
" > ${HADOOP_CODE_PATH}'/etc/hadoop/mapred-site.xml'

# * etc/hadoop/yarn-site.xml
sed -i '/^[ \t]*<\/configuration>[ \t]*/d' ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'
NUM=`grep -m 1 -n '<name>yarn.nodemanager.aux-services</name>' ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml' | cut -d ':' -f 1`
if [[ -n ${NUM} ]]; then
    sed -i "`echo ${NUM}-1|bc`,`echo ${NUM}+2|bc`d" ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'
fi
NUM=`grep -m 1 -n '<name>yarn.nodemanager.env-whitelist</name>' ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml' | cut -d ':' -f 1`
if [[ -n ${NUM} ]]; then
    sed -i "`echo ${NUM}-1|bc`,`echo ${NUM}+2|bc`d" ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'
fi

echo -e "\
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
" >> ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'

# * delete blank lines
sed -i '/^[ \t]*$/d' ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'

