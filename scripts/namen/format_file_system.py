#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.add_user_group <--')

        ssh_option = 'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5'

        #
        # clear hdfs
        #
        host_list = self.getHosts()

        remote_ins = "rm -rf {0}/{1}/* {0}/{2}/* {0}/{3}/*".format(
            self.ys['binarycode'], self.ys['roles']['namen']['dir'],
            self.ys['roles']['namen']['sdir'], self.ys['roles']['datan']['dir'])

        for host in host_list:
            ins = "{0} {2}@{1} -tt '{3}' ".format(
                ssh_option, host['ip'], host['usr'],
                remote_ins)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # formate
        #
        dest_folder = os.path.join(self.ys['binarycode'], 'rose-on-yarn/')

        ins = "{0} {2}@{1} -tt '{3}/bin/hdfs namenode -format -force' ".format(
            ssh_option, self.ys['roles']['namen']['hosts'][0],
            self.ys['roles']['namen']['usr'], dest_folder)

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
