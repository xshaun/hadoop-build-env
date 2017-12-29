#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.install_runtime_prerequisties <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        cluster_script_dir = self.getClusterScriptDir()

        #
        # build master and slaves environment
        #

        remote_ins = os.path.join(
            cluster_script_dir, 'install_runtime_prerequisites.sh')

        instructions = list()
        for host in host_list:
            ins = "ssh {0} {2}@{1} -tt 'sudo -S {3}'".format(
                ssh_option, host['ip'], host['usr'],
                remote_ins)

            instructions.append((ins, host['pwd']))

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
