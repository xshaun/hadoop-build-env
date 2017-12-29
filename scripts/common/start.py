#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def __parse(self, param):
        cluster_binary_dir = self.getClusterBinaryDir()

        if 'hdfs' == param:
            return os.path.join(
                cluster_binary_dir, 'sbin/start-dfs.sh')

        if 'yarn' = os.path.join(
            cluster_binary_dir, 'sbin/start-yarn.sh')

        if 'jobhistory' == param:
            return os.path.join(
                cluster_binary_dir, 'bin/mapred --daemon start historyserver')

        # TODO, add more
        return

    def action(self):
        logger.info('--> common.start <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        rm_list = self.getHosts(roles=['resourcem', ])

        params = self.ys['params']
        candidates = list()

        if len(params) == 0:
            params.append('hdfs')
            params.append('yarn')
            params.append('jobhistory')

        for p in params:
            candidates.append(self.__parse(p))

        instructions = list()
        for host in rm_list:
            #!!! donot use -tt option
            ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                ssh_option, host['ip'], host['usr'],
                ' && '.join(candidates))

            instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
