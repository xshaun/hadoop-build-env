#!/bin/bash

# -----------------------------
# >> User vars <<

# Recent released version
# [
# * HADOOP_VERSION='2.5.2'
# * HADOOP_VERSION='2.6.5'
# * HADOOP_VERSION='2.7.3'
# * HADOOP_VERSION='2.8.0'
# * HADOOP_VERSION='3.0.0-alpha1'
HADOOP_VERSION='3.0.0-alpha2'
# ]

# Hadoop Code
HADOOP_CODE_LOCATION=`cd ~;pwd`     # default
HADOOP_CODE_PATH=${HADOOP_CODE_LOCATION}'/hadoop-'${HADOOP_VERSION}
mkdir -p ${HADOOP_CODE_PATH}

# Hadoop cluster mode
# [
# * HADOOP_CLUSTER_MODE='LOCAL_MODE' # not support now
HADOOP_CLUSTER_MODE='PSEUDO_DIS_MODE'
# * HADOOP_CLUSTER_MODE='FULLY_DIS_MODE'
# ]


# -----------------------------
# >> Hadoop original env vars <<

# Hadoop Opportunistic container enable/disable
HADOOP_OPPORTUNISTIC_CONTAINER_ENABLE=true

# Hadoop Distributed scheduling enable/disbale
HADOOP_DISTRIBUTED_SCHEDULING_ENABLE=false

# Secure and insecure env vars
# * [start|stop]-dfs.sh
HDFS_DATANODE_USER=root
HADOOP_SECURE_DN_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
#
# * [start|stop]-yarn.sh
YARN_NODEMANAGER_USER=root
YARN_RESOURCEMANAGER_USER=root

