#!/bin/bash
#
source 0.*

# ----------------------------
# Edit the files <hadoop code path>/[etc, bin, share...]
#   to define some parameters as follows:
#
# FILE: etc/hadoop/hadoop-env.sh
#
FILE=${HADOOP_CODE_PATH}'/etc/hadoop/hadoop-env.sh'
# * set to the root of your Java installation
put_config_line --file ${FILE} --property 'JAVA_HOME' --value ${JAVA_HOME} --prefix 'export'

#
# FILE: sbin/[start|stop]-dfs.sh
#
ls ${HADOOP_CODE_PATH}/sbin/*-dfs.sh | cat | while read FILE ; do
    arr=(
        "HDFS_DATANODE_USER"
        "HADOOP_SECURE_DN_USER"
        "HDFS_NAMENODE_USER"
        "HDFS_SECONDARYNAMENODE_USER"
        )
    for item in ${arr[@]}; do
        put_config_line --file ${FILE} --property ${item} --value ${!item}
    done
done

#
# FILE: sbin/[start|stop]-yarn.sh
#
ls ${HADOOP_CODE_PATH}/sbin/*-yarn.sh | cat | while read FILE ; do
    arr=(
        "YARN_NODEMANAGER_USER"
        "YARN_RESOURCEMANAGER_USER"
        )
    for item in ${arr[@]}; do
        put_config_line --file ${FILE} --property ${item} --value ${!item}
    done
done

