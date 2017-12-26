#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns
import os


class Custom(Basis):

    def __parse(self, param):
        if 'hdfs' == param:
            return 'sbin/stop-dfs.sh'

        if 'yarn' == param:
            return 'sbin/stop-yarn.sh'

        # TODO, add more
        return

    def action(self):
        logger.info('--> common.stop <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        rm_list = self.getHosts(roles=['resourcem', ])

        cluster_script_dir = self.getClusterScriptDir()

        candidates = list()
        for p in self.ys['params']:
            candidates.append(os.path.join(
                cluster_script_dir, self.__parse(p)))

        if len(candidates) == 0:
            candidates.append(os.path.join(
                cluster_script_dir, 'sbin/stop-all.sh'))

        threads = list()
        for host in rm_list:
            #!!! donot use -tt option
            ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                ssh_option, host['ip'], host['usr'],
                ' && '.join(candidates))

            t = ParaIns(ins)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = t.ret == ret
        return ret


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
