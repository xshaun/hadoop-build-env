#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd


class Custom(Basis):

    def action(self):
        logger.info('--> common.stop_all <--')

        ssh_option = 'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts(roles=['resourcem', ])

        dest_folder = os.path.join(self.ys['binarycode'], 'rose-on-yarn/')

        for host in host_list:
            ins = "{0} {2}@{1} -tt '{3}/sbin/stop-all.sh' ".format(
                ssh_option, host['ip'], host['usr'],
                dest_folder)

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
