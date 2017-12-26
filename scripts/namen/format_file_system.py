#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.format_file_system <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        cluster_binary_dir = self.getClusterBinaryDir()
        cluster_hdfs_dir = self.getClusterHdfsDir()

        #
        # stop all deamons
        #
        remote_ins = "{0} && {0}".format(
            os.path.join(cluster_binary_dir, 'sbin/stop-all.sh'))

        ins = "ssh {0} {2}@{1} -tt '{3}' ".format(
            ssh_option, self.ys['roles']['namen']['hosts'][0],
            self.ys['roles']['namen']['usr'], remote_ins)

        retcode = cmd.do(ins)

        logger.info("ins: %s; retcode: %d." % (ins, retcode))

        #
        # clear hdfs files
        #
        """
        folders for namenode
        """
        name_nodes = self.getHosts(roles=['namen', ])

        namefiles = os.path.join(cluster_hdfs_dir,
                                 self.ys['roles']['namen']['dir'], '*')
        namesfiles = os.path.join(cluster_hdfs_dir,
                                  self.ys['roles']['namen']['sdir'], '*')

        for host in name_nodes:
            ins = "ssh {0} {2}@{1} -tt 'rm -rf {3} {4}' ".format(
                ssh_option, host['ip'], host['usr'],
                namefiles, namesfiles)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        """
        folders for datanodes
        """
        data_nodes = self.getHosts(roles=['datan', ])

        datafiles = os.path.join(cluster_hdfs_dir,
                                 self.ys['roles']['datan']['dir'], '*')

        for host in data_nodes:
            ins = "ssh {0} {2}@{1} -tt 'rm -rf {3}' ".format(
                ssh_option, host['ip'], host['usr'],
                datafiles)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # formate
        #
        remote_ins = "{0} namenode -format -force".format(
            os.path.join(cluster_binary_dir, 'bin/hdfs'))

        ins = "ssh {0} {2}@{1} -tt '{3}' ".format(
            ssh_option, self.ys['roles']['namen']['hosts'][0],
            self.ys['roles']['namen']['usr'], remote_ins)

        retcode = cmd.do(ins)

        logger.info("ins: %s; retcode: %d." % (ins, retcode))

        if retcode != 0:
            logger.error(ins)
            return False

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
