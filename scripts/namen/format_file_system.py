#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.format_file_system <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        cluster_binary_dir = self.getClusterBinaryDir()

        #
        # clear hdfs files
        #
        """
        folders for namenode
        """
        name_nodes = self.getHosts(roles=['namen', ])

        namefiles = os.path.join(self.getClusterHdfsDir(
            subdir=self.ys['roles']['namen']['dir']), '*')
        namesfiles = os.path.join(self.getClusterHdfsDir(
            subdir=self.ys['roles']['namen']['sdir']), '*')

        instructions = list()
        for host in name_nodes:
            ins = "ssh {0} {2}@{1} -tt 'rm -rf {3} {4}' ".format(
                ssh_option, host['ip'], host['usr'],
                namefiles, namesfiles)

            instructions.append(ins)

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        """
        folders for datanodes
        """
        data_nodes = self.getHosts(roles=['datan', ])

        datafiles = os.path.join(self.getClusterHdfsDir(
            subdir=self.ys['roles']['datan']['dir']), '*')

        instructions = list()
        for host in data_nodes:
            ins = "ssh {0} {2}@{1} -tt 'rm -rf {3}' ".format(
                ssh_option, host['ip'], host['usr'],
                datafiles)

            instructions.append(ins)

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        #
        # formate
        #
        remote_ins = "{0} namenode -format -force".format(
            os.path.join(cluster_binary_dir, 'bin/hdfs'))

        ins = "ssh {0} {2}@{1} -tt '{3}' ".format(
            ssh_option, self.ys['roles']['namen']['hosts'][0],
            self.ys['roles']['namen']['usr'], remote_ins)

        return 0 == Command.do(ins)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
