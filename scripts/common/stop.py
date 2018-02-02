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
                cluster_binary_dir, 'sbin/stop-dfs.sh')

        if 'yarn' == param:
            return os.path.join(
                cluster_binary_dir, 'sbin/stop-yarn.sh')

        if 'jobhistory' == param:
            return os.path.join(
                cluster_binary_dir, 'bin/mapred --daemon stop historyserver')

        if 'timelineserver' == param:
            return os.path.join(
                cluster_binary_dir, 'bin/yarn --daemon stop timelineserver')

        # TODO, add more
        return

    def action(self):
        logger.info('--> common.stop <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        host_list = self.getHosts()
        rm_list = self.getHosts(roles=['resourcem', ])

        # -- step1
        params = self.getParams()

        if len(params) == 0:
            params.append('hdfs')
            params.append('yarn')
            params.append('jobhistory')
            params.append('timelineserver')

        # -- step2
        EACH_HOST_INS = [] # such as 'nodemanager' and datanode

        instructions = list()

        for p in params:
            tlist = None
            if p in EACH_HOST_INS:
                tlist = host_list
            else:
                tlist = rm_list

            for host in tlist:
                if self.__parse(p) is None:
                    continue

                #!!! donot use -tt option
                ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                    ssh_option, host['ip'], host['usr'],
                    self.__parse(p))
                instructions.append(ins)

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        # -- step3 : remove 'process information unavailable'
        if len(self.getParams()) == 0:
            instructions = list()

            for host in host_list:
                ins = "ssh {0} {2}@{1} -tt 'sudo -S rm -rf /tmp/hsperfdata*'".format(
                    ssh_option, host['ip'], host['usr'])

                instructions.append((ins, host['pwd']))

            ret = Command.parallel(instructions)

        return ret

def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
