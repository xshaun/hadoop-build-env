#!/bin/bash
#
source 0.*


if [[ ! -f "${HADOOP_SRC_CODE_PATH}/hadoop-dist/target/hadoop-${HADOOP_VERSION}.tar.gz" ]]; then
    echo "Can not find 'hadoop-${HADOOP_VERSION}.tar.gz' in '${HADOOP_SRC_CODE_PATH}/hadoop-dist/target/' "
    echo "Please run 'mvn package -Pdist -DskipTests -Dtar -Dmaven.javadoc.skip=true' in '${HADOOP_SRC_CODE_PATH}' "
    echo " or run 'mvn package -Pdist,native,docs,src -DskipTests -Dtar' in '${HADOOP_SRC_CODE_PATH}' "
fi

if [[ 'PSEUDO_DIS_MODE' == ${HADOOP_CLUSTER_MODE} ]]; then
    cd ${HADOOP_SRC_CODE_PATH}/hadoop-dist/target && \
    tar -zxv -C ${HADOOP_CODE_LOCATION} -f ${HADOOP_SRC_CODE_PATH}/hadoop-dist/target/hadoop-${HADOOP_VERSION}.tar.gz hadoop-${HADOOP_VERSION}/share/* && \
    cd -
fi
