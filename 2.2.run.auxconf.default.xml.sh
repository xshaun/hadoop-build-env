#!/bin/bash
#
source 0.*

set -e

# Default XML
cp ./default-xml/core-default.xml ${HADOOP_CODE_PATH}'/etc/hadoop/core-site.xml'
cp ./default-xml/hdfs-default.xml ${HADOOP_CODE_PATH}'/etc/hadoop/hdfs-site.xml'
cp ./default-xml/yarn-default.xml ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'
cp ./default-xml/mapred-default.xml ${HADOOP_CODE_PATH}'/etc/hadoop/mapred-site.xml'

# >> Pseudo-Distributed Operation <<
#
if [[ 'PSEUDO_DIS_MODE' == ${HADOOP_CLUSTER_MODE} ]]; then

    # * etc/hadoop/core-site.xml
    put_config_xml  \
        --file ${HADOOP_CODE_PATH}'/etc/hadoop/core-site.xml'   \
        --property 'fs.defaultFS'   \
        --value 'hdfs://localhost:9000'

    # * etc/hadoop/hdfs-site.xml
    mkdir -p ${HADOOP_CODE_LOCATION}'/hadoop_mydata/hdfs/namenode'
    mkdir -p ${HADOOP_CODE_LOCATION}'/hadoop_mydata/hdfs/datanode'

    put_config_xml  \
        --file ${HADOOP_CODE_PATH}'/etc/hadoop/hdfs-site.xml'   \
        --property 'dfs.replication'   \
        --value '1'

    put_config_xml  \
        --file ${HADOOP_CODE_PATH}'/etc/hadoop/hdfs-site.xml'   \
        --property 'dfs.namenode.name.dir'   \
        --value "file:${HADOOP_CODE_LOCATION}/hadoop_mydata/hdfs/namenode"

    put_config_xml  \
        --file ${HADOOP_CODE_PATH}'/etc/hadoop/hdfs-site.xml'   \
        --property 'dfs.datanode.data.dir'   \
        --value "file:${HADOOP_CODE_LOCATION}/hadoop_mydata/hdfs/datanode"

    # *Format the filesystem:
    ${HADOOP_CODE_PATH}/bin/hdfs namenode -format -nonInteractive


    if [[ '3.0.0-alpha2' == ${HADOOP_VERSION} ]]; then
        # Enabling Opportunistic Containers
        #
        put_config_xml  \
            --file ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'   \
            --property 'yarn.resourcemanager.opportunistic-container-allocation.enabled'   \
            --value "${HADOOP_OPPORTUNISTIC_CONTAINER_ENABLE}"

        put_config_xml  \
            --file ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'   \
            --property 'yarn.nodemanager.opportunistic-containers-max-queue-length'   \
            --value '20'

        # Distributed scheduling
        #
        put_config_xml  \
            --file ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'   \
            --property 'yarn.nodemanager.distributed-scheduling.enabled'   \
            --value "${HADOOP_DISTRIBUTED_SCHEDULING_ENABLE}"

        put_config_xml  \
            --file ${HADOOP_CODE_PATH}'/etc/hadoop/yarn-site.xml'   \
            --property 'yarn.nodemanager.amrmproxy.enabled'   \
            --value "${HADOOP_DISTRIBUTED_SCHEDULING_ENABLE}"
    fi

fi
