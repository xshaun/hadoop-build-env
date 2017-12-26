#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.distribute_binary_package_prep <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        cluster_script_dir = self.getClusterScriptDir()
        cluster_binary_dir = self.getClusterBinaryDir()
        cluster_hdfs_dir = self.getClusterHdfsDir()

        sourcecode = self.ys['sourcecode']
        binarycode = self.ys['binarycode']

        #
        # add permissions
        #
        for host in host_list:
            """
            create folders
            """
            ins = "ssh {0} {2}@{1} -tt 'sudo -S mkdir -p {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

            """
            chown
            """
            ins = "ssh {0} {2}@{1} -tt 'sudo -S chown -R {2} {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

            """
            chmod
            """
            ins = "ssh {0} {2}@{1} -tt 'sudo -S chmod -R 777 {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # create hdfs folders
        #

        """
        folders for namenode
        """
        name_nodes = self.getHosts(roles=['namen', ])

        namedir = os.path.join(cluster_hdfs_dir,
                               self.ys['roles']['namen']['dir'])
        namesdir = os.path.join(cluster_hdfs_dir,
                                self.ys['roles']['namen']['sdir'])

        for host in name_nodes:
            ins = "ssh {0} {2}@{1} -tt 'mkdir -p {3} {4}' ".format(
                ssh_option, host['ip'], host['usr'], namedir, namesdir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        """
        folders for datanodes
        """
        data_nodes = self.getHosts(roles=['datan', ])

        datadir = os.path.join(cluster_hdfs_dir,
                               self.ys['roles']['datan']['dir'])

        for host in data_nodes:
            ins = "ssh {0} {2}@{1} -tt 'mkdir -p {3}' ".format(
                ssh_option, host['ip'], host['usr'], datadir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # scripts about building env
        #
        hbe_utilities = './utilities/*'

        for host in host_list:
            ins = ("ssh {0} {2}@{1} -tt 'mkdir -p {4}' "
                   "&& scp -r {0} {3} {2}@{1}:{4} ").format(
                ssh_option, host['ip'], host['usr'],
                hbe_utilities, cluster_script_dir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # config setup_passphraseless from master to slaves
        #
        setup_passphraseless = os.path.join(
            cluster_script_dir, 'setup_passphraseless.sh')

        # hdfs
        namenode = self.getHosts(roles=['namen', ])
        datanodes = self.getHosts(roles=['datan', ])

        datanodes_hostname = list()
        for host in datanodes:
            datanodes_hostname.append("%s@%s" % (host['usr'], host['ip']))

        for host in namenode:
            ins = "ssh {0} {2}@{1} -tt '{3} \'{4}\' \'{5}\'' ".format(
                ssh_option, host['ip'], host['usr'],
                setup_passphraseless, ",".join(datanodes_hostname),
                self.ys['roles']['datan']['pwd'])

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        # yarn
        resourcemanager = self.getHosts(roles=['resourcem', ])
        nodemanagers = self.getHosts(roles=['nodem', ])

        nodemanagers_hostname = list()
        for host in nodemanagers:
            nodemanagers_hostname.append("%s@%s" % (host['usr'], host['ip']))

        for host in resourcemanager:
            ins = "ssh {0} {2}@{1} -tt '{3} \'{4}\' \'{5}\''".format(
                ssh_option, host['ip'], host['usr'],
                setup_passphraseless, ",".join(nodemanagers_hostname),
                self.ys['roles']['nodem']['pwd'])

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # wait to end
        #
        ins = 'wait'
        retcode = cmd.do(ins)
        if retcode != 0:
            logger.error(ins)
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
