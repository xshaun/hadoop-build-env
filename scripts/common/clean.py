#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command


class Custom(Basis):

    def __parse(self, param):
        if 'log' == param:
            return "cd {0} && for l in `ls ./*.log`; do echo \'\' > $l ; done".format(
                self.getClusterLogDir())

        # TODO, add more
        return

    def action(self):
        logger.info('--> common.clean <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        host_list = self.getHosts()

        cluster_script_dir = self.getClusterScriptDir()

        instructions = list()

        params = self.ys['params']
        if len(params) == 0:
            params.append('log')

        for p in self.ys['params']:
            remote_ins = self.__parse(p)

            for host in host_list:
                #!!! donot use -tt option
                ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                    ssh_option, host['ip'], host['usr'],
                    remote_ins)

                instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
