#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


def putconfig(file, name, value):
    root = ElementTree.parse(file).getroot()

    description = ''
    for existing_prop in root.getchildren():
        if existing_prop.find('name').text == name:
            description = existing_prop.find('description').text
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

    conf_file = open(file, 'w')
    conf_file.write(ElementTree.tostring(root))
    conf_file.close()


class Custom(Basis):

    def action(self):
        logger.info('--> common.configure_site_xml <--')

        #
        # wirte slaves' ip into workers
        #
        host_list = self.getSlaveHosts()

        workers = open('./configs/workers', 'w')
        for host in host_list:
            workers.write(host['ip'])
        workers.close()

        #
        # configure *-site.xml
        #
        putconfig(file='./configs/core-site.xml',
                  name='fs.defaultFS',
                  value="hdfs://%s:9000" % self.ys['roles']['namen']['hosts'][0])

        putconfig(file='./configs/hdfs-site.xml',
                  name='dfs.replication',
                  value='1')

        putconfig(file='./configs/hdfs-site.xml',
                  name='dfs.namenode.name.dir',
                  value=os.path.join('file:',
                                     self.ys['binarycode'],
                                     self.ys['roles']['namen']['dir']))

        putconfig(file='./configs/hdfs-site.xml',
                  name='fs.checkpoint.dir',
                  value=os.path.join('file:',
                                     self.ys['binarycode'],
                                     self.ys['roles']['namen']['sdir']))

        putconfig(file='./configs/hdfs-site.xml',
                  name='fs.checkpoint.edits.dir',
                  value=os.path.join('file:',
                                     self.ys['binarycode'],
                                     self.ys['roles']['namen']['sdir']))

        putconfig(file='./configs/hdfs-site.xml',
                  name='dfs.datanode.data.dir',
                  value=os.path.join('file:',
                                     self.ys['binarycode'],
                                     self.ys['roles']['datan']['dir']))

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

        # --- mr
        putconfig(file='./configs/mapred-site.xml',
                  name='mapreduce.framework.name',
                  value='yarn')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.aux-services',
                  value='mapreduce_shuffle')

        putconfig(file='./configs/yarn-site.xml',
                  name='yarn.nodemanager.env-whitelist',
                  value='JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME')

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
