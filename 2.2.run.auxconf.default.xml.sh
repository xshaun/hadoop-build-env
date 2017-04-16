#!/bin/bash
#
source 0.*

# >> Pseudo-Distributed Operation <<
#
if [[ 'PSEUDO_DIS_MODE' == $HADOOP_CLUSTER_MODE ]]; then

# * etc/hadoop/core-site.xml
echo """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
""" > $HADOOP_CODE_PATH'/etc/hadoop/core-site.xml'

# * etc/hadoop/hdfs-site.xml
mkdir -p ${HADOOP_CODE_LOCATION}'/hadoop_mydata/hdfs/namenode'
mkdir -p ${HADOOP_CODE_LOCATION}'/hadoop_mydata/hdfs/datanode'

echo """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:"""${HADOOP_CODE_LOCATION}'/hadoop_mydata/hdfs/namenode'"""</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:"""${HADOOP_CODE_LOCATION}'/hadoop_mydata/hdfs/datanode'"""</value>
    </property>
</configuration>
""" > $HADOOP_CODE_PATH'/etc/hadoop/hdfs-site.xml'

# *Format the filesystem:
$HADOOP_CODE_PATH'/bin/hdfs' namenode -format

# * Make the HDFS directories required to execute MapReduce jobs:
$HADOOP_CODE_PATH'/bin/hdfs' dfs -mkdir /user
$HADOOP_CODE_PATH'/bin/hdfs' dfs -mkdir /user/root

# MR on yarn
#
# * etc/hadoop/mapred-site.xml
echo """
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
""" > $HADOOP_CODE_PATH'/etc/hadoop/mapred-site.xml'
# * etc/hadoop/yarn-site.xml
echo """
<?xml version="1.0"?>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
""" > $HADOOP_CODE_PATH'/etc/hadoop/yarn-site.xml'

fi

if [[ '3.0.0-alpha2' == $HADOOP_VERSION ]]; then
# Enabling Opportunistic Containers
#
# * etc/hadoop/yarn-site.xml
echo """
    <property>
        <name>yarn.resourcemanager.opportunistic-container-allocation.enabled</name>
        <value>"""$HADOOP_OPPORTUNISTIC_CONTAINER_ENABLE"""</value>
    </property>
    <property>
        <name>yarn.nodemanager.opportunistic-containers-max-queue-length</name>
        <value>20</value>
    </property>
""" >> $HADOOP_CODE_PATH'/etc/hadoop/yarn-site.xml'
# Distributed scheduling
#
# * etc/hadoop/yarn-site.xml
echo """
    <property>
        <name>yarn.nodemanager.distributed-scheduling.enabled</name>
        <value>"""$HADOOP_DISTRIBUTED_SCHEDULING_ENABLE"""</value>
    </property>
    <property>
        <name>yarn.nodemanager.amrmproxy.enabled</name>
        <value>"""$HADOOP_DISTRIBUTED_SCHEDULING_ENABLE"""</value>
    </property>
""" >> $HADOOP_CODE_PATH'/etc/hadoop/yarn-site.xml'

fi

echo """
</configuration>
""" >> $HADOOP_CODE_PATH'/etc/hadoop/yarn-site.xml'
