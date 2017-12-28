#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns
import os
import shutil
from lxml import etree as ElementTree
from lxml.etree import Element as Element
from lxml.etree import SubElement as SubElement


#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


def putconfig(file, name, value):
    root = ElementTree.parse(file).getroot()

    description = ''
    for existing_prop in root.getchildren():
        ename = existing_prop.find('name')
        if ename is not None and ename.text == name:
            edescription = existing_prop.find('description')
            if edescription is not None:
                description = edescription.text
            root.remove(existing_prop)
            break

    property = SubElement(root, 'property')
    if description != '':
        description_elem = SubElement(property, 'description')
        description_elem.text = description

    name_elem = SubElement(property, 'name')
    name_elem.text = name
    value_elem = SubElement(property, 'value')
    value_elem.text = value

    conf_file = open(file, 'wb')
    conf_file.write(ElementTree.tostring(
        root, pretty_print=True, encoding='utf-8'))
    conf_file.close()

    return


class Custom(Basis):

    def action(self):
        logger.info('--> common.configure_site <--')

        cluster_hadoop_lib_native = self.getClusterHadoopLibNativeDir()
        cluster_hadoop_conf_dir = self.getClusterHadoopConfDir()
        cluster_binary_dir = self.getClusterBinaryDir()
        cluster_hdfs_dir = self.getClusterHdfsDir()
        cluster_log_dir = self.getClusterLogDir()

        controlp_binary_dir = self.getControlPBinaryDir()

        #
        # wirte slaves' ip into workers
        #
        slaves_list = self.getSlaveHosts()

        workers = open('./configs/workers', 'w')
        for host in slaves_list:
            workers.write("%s \n" % (host['ip']))
        workers.close()

        #
        # configure *-site.xml
        #
        shutil.copy2('./configs/default/hadoop-core.xml',
                     './configs/core-site.xml')
        shutil.copy2('./configs/default/hadoop-hdfs.xml',
                     './configs/hdfs-site.xml')
        shutil.copy2('./configs/default/hadoop-yarn.xml',
                     './configs/yarn-site.xml')
        shutil.copy2('./configs/default/hadoop-mapred.xml',
                     './configs/mapred-site.xml')

        putconfig(file='./configs/core-site.xml',
                  name='fs.defaultFS',
                  value="hdfs://%s:9000" % self.ys['roles']['namen']['hosts'][0])

        putconfig(file='./configs/hdfs-site.xml',
                  name='dfs.replication',
                  value='1')

        putconfig(file='./configs/hdfs-site.xml',
                  name='dfs.namenode.name.dir',
                  value=os.path.join('file:', cluster_hdfs_dir,
                                     self.ys['roles']['namen']['dir']))

        putconfig(file='./configs/hdfs-site.xml',
                  name='fs.checkpoint.dir',
                  value=os.path.join('file:', cluster_hdfs_dir,
                                     self.ys['roles']['namen']['sdir']))

        putconfig(file='./configs/hdfs-site.xml',
                  name='fs.checkpoint.edits.dir',
                  value=os.path.join('file:', cluster_hdfs_dir,
                                     self.ys['roles']['namen']['sdir']))

        putconfig(file='./configs/hdfs-site.xml',
                  name='dfs.datanode.data.dir',
                  value=os.path.join('file:', cluster_hdfs_dir,
                                     self.ys['roles']['datan']['dir']))

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.resourcemanager.hostname',
                  value=self.ys['roles']['resourcem']['hosts'][0])

        # support distributed scheduler
        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.resourcemanager.opportunistic-container-allocation.enabled',
                  value='true')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.opportunistic-containers-max-queue-length',
                  value='20')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.distributed-scheduling.enabled',
                  value='true')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.amrmproxy.enabled',
                  value='true')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.amrmproxy.address',
                  value='0.0.0.0:8049')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.resourcemanager.scheduler.address',
                  value='0.0.0.0:8049') # NMs  -> we need to change it into rm-ip:8030 on RM

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.amrmproxy.realrm.scheduler.address',
                  value="%s:8030" % self.ys['roles']['resourcem']['hosts'][0])

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.amrmproxy.client.thread-count',
                  value='3')

        # mapreduce
        putconfig(file='./configs/mapred-site.xml',
                  name='mapreduce.framework.name',
                  value='yarn')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.aux-services',
                  value='mapreduce_shuffle')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.env-whitelist',
                  value='JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME')

        ins = "format_file %s && format_file %s && format_file %s && format_file %s" % (
            './configs/core-site.xml',
            './configs/hdfs-site.xml',
            './configs/yarn-site.xml',
            './configs/mapred-site.xml')

        retcode = cmd.do(ins)

        logger.info("ins: %s; retcode: %d." % (ins, retcode))

        if retcode != 0:
            logger.error(ins)
            return False

        #
        # configure ./etc/hadoop/*.sh
        #
        hadoop_env_file = os.path.join(
            controlp_binary_dir, 'etc/hadoop/hadoop-env.sh')

        ins = ':'
        envlist = [
            ['PDSH_RCMD_TYPE', 'ssh'],
            ['JAVA_HOME', '/usr/lib/jvm/java-8-openjdk-amd64/'],
            ['HADOOP_HOME', cluster_binary_dir],
            ['HADOOP_YARN_HOME', cluster_binary_dir],
            ['HADOOP_HDFS_HOME', cluster_binary_dir],
            ['HADOOP_MAPRED_HOME', cluster_binary_dir],
            ['HADOOP_COMMON_HOME', cluster_binary_dir],
            ['HADOOP_COMMON_LIB_NATIVE_DIR', cluster_hadoop_lib_native],
            ['HADOOP_OPTS',
                "'\"${HADOOP_OPTS} -Djava.library.path=%s\"'" % (cluster_hadoop_lib_native)],
            ['HADOOP_CONF_DIR', cluster_hadoop_conf_dir],
            ['HADOOP_LOG_DIR', cluster_log_dir],                 # custom
            ['HADOOP_ROOT_LOGGER', 'DEBUG,console,RFA'],         # DEBUG mode custom
            ['HADOOP_DAEMON_ROOT_LOGGER', 'DEBUG,console,RFA'],  # DEBUG mode custom
            ['HADOOP_SECURITY_LOGGER', 'DEBUG,console,RFA'],     # DEBUG mode custom
            # ['YARN_CONF_DIR', cluster_hadoop_conf_dir],        # Deprecated
            # ['YARN_ROOT_LOGGER', 'DEBUG,console,RFA'],         # Deprecated
        ]

        for e in envlist:
            ins += " && put_config_line --file {0} --property {1} --value {2} --prefix 'export' ".format(
                hadoop_env_file, e[0], e[1])

        retcode = cmd.do(ins)

        logger.info("ins: %s; retcode: %d." % (ins, retcode))

        if retcode != 0:
            logger.error(ins)
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
