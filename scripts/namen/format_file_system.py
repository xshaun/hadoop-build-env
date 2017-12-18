#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.format_file_system <--')

        ssh_option = 'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5'

        sourcecode = self.ys['sourcecode']
        binarycode = self.ys['binarycode']

        #
        # clear hdfs
        #
        """
        folders for namenode
        """
        name_nodes = self.getHosts(roles=['namen', ])

        namedir = os.path.join(binarycode,
                               self.ys['roles']['namen']['dir'], '*')
        namesdir = os.path.join(binarycode,
                                self.ys['roles']['namen']['sdir'], '*')

        for host in name_nodes:
            ins = "{0} {2}@{1} -tt 'rm -rf {3} {4}' & sleep 0.5".format(
                ssh_option, host['ip'], host['usr'],
                namedir, namesdir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        """
        folders for datanodes
        """
        data_nodes = self.getHosts(roles=['datan', ])

        datadir = os.path.join(binarycode,
                               self.ys['roles']['datan']['dir'], '*')

        for host in data_nodes:
            ins = "{0} {2}@{1} -tt 'rm -rf {3}' & sleep 0.5".format(
                ssh_option, host['ip'], host['usr'],
                datadir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # formate
        #
        dest_folder = os.path.join(binarycode, 'rose-on-yarn/')

        remote_ins = "{0} && {0} && {1} namenode -format -force".format(
            os.path.join(dest_folder, 'sbin/stop-all.sh')
            os.path.join(dest_folder, 'bin/hdfs'))

        ins = "{0} {2}@{1} -tt '{3}' ".format(
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
