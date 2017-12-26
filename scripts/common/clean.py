#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    def __parse(self, param):
        if param is 'log':
            return "cd {0} && for l in `ls ./*.log`; do echo \'\' > $l ; done".format(
                self.getClusterLogDir())

        # TODO, add more
        return

    # override
    def action(self):
        logger.info('--> common.clean <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        rm_list = self.getHosts(roles=['resourcem', ])

        cluster_script_dir = self.getClusterScriptDir()

        for p in self.ys['params']:
            remote_ins = self.__parse(p)

            for host in rm_list:
                #!!! donot use -tt option
                ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                    ssh_option, host['ip'], host['usr'],
                    remote_ins)

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
