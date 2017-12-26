#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    def __parse(self, param):
        if param is 'hdfs':
            return 'sbin/stop-dfs.sh'

        if param is 'yarn':
            return 'sbin/stop-yarn.sh'

        # TODO, add more
        return

    def action(self):
        logger.info('--> common.stop <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        rm_list = self.getHosts(roles=['resourcem', ])

        cluster_script_dir = self.getClusterScriptDir()

        remote_ins = list()
        if self.ys['params'] == 0:
            remote_ins.append(os.path.join(
                cluster_script_dir, 'sbin/stop-all.sh'))
        else:
            for p in self.ys['params']:
                remote_ins.append(os.path.join(
                    cluster_script_dir, self.__parse(p)))

        for host in rm_list:
            #!!! donot use -tt option
            ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                ssh_option, host['ip'], host['usr'],
                ' && '.join(remote_ins))

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
