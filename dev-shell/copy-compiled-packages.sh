# -----------------------------------------------------------
YARN_SOURCE_PATH='./hadoop-3.0.0-alpha2-src/hadoop-yarn-project/hadoop-yarn'
YARN_TARGET_PATH='./hadoop-3.0.0-alpha2/share/hadoop/yarn/'

cp ${YARN_SOURCE_PATH}/hadoop-yarn-api/target/hadoop-yarn-api-3.0.0-alpha2.jar ${YARN_TARGET_PATH}

cp ${YARN_SOURCE_PATH}/hadoop-yarn-applications/hadoop-yarn-applications-distributedshell/target/hadoop-yarn-applications-distributedshell-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-applications/hadoop-yarn-applications-unmanaged-am-launcher/target/hadoop-yarn-applications-unmanaged-am-launcher-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
  
cp ${YARN_SOURCE_PATH}/hadoop-yarn-client/target/hadoop-yarn-client-3.0.0-alpha2.jar ${YARN_TARGET_PATH}

cp ${YARN_SOURCE_PATH}/hadoop-yarn-common/target/hadoop-yarn-common-3.0.0-alpha2.jar ${YARN_TARGET_PATH}

cp ${YARN_SOURCE_PATH}/hadoop-yarn-registry/target/hadoop-yarn-registry-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-registry/target/hadoop-yarn-registry-3.0.0-alpha2.jar ${YARN_TARGET_PATH}

cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-applicationhistoryservice/target/hadoop-yarn-server-applicationhistoryservice-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-common/target/hadoop-yarn-server-common-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-nodemanager/target/hadoop-yarn-server-nodemanager-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-sharedcachemanager/target/hadoop-yarn-server-sharedcachemanager-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-tests/target/hadoop-yarn-server-tests-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-timeline-pluginstorage/target/hadoop-yarn-server-timeline-pluginstorage-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-timelineservice/target/hadoop-yarn-server-timelineservice-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-timelineservice-hbase/target/hadoop-yarn-server-timelineservice-hbase-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-timelineservice-hbase-tests/target/hadoop-yarn-server-timelineservice-hbase-tests-3.0.0-alpha2.jar ${YARN_TARGET_PATH}
cp ${YARN_SOURCE_PATH}/hadoop-yarn-server/hadoop-yarn-server-web-proxy/target/hadoop-yarn-server-web-proxy-3.0.0-alpha2.jar ${YARN_TARGET_PATH}