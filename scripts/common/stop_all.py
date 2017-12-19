#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.stop_all <--')

        ssh_option = 'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=600'

        host_list = self.getHosts(roles=['resourcem', ])

        dest_folder = os.path.join(self.ys['binarycode'], 'rose-on-yarn/')

        for host in host_list:
            #!!! donot use -tt option
            ins = "{0} {2}@{1} -T '{3} && {4}' ".format(
                ssh_option, host['ip'], host['usr'],
                os.path.join(dest_folder, 'sbin/stop-yarn.sh'),
                os.path.join(dest_folder, 'sbin/stop-dfs.sh'))

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
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
