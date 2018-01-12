#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.change_binarycode_mode_own <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        cluster_binary_dir = self.getClusterBinaryDir()
        cluster_script_dir = self.getClusterScriptDir()

        remote_ins = "sudo -S %s %s %s %s" % (
            os.path.join(cluster_script_dir, 'change_binarycode_mode_own.sh'),
            self.ys['opt']['group'], self.ys['opt']['user'],
            cluster_binary_dir)

        instructions = list()
        for host in host_list:
            ins = "ssh {0} {2}@{1} -tt '{3}' ".format(
                ssh_option, host['ip'], host['usr'],
                remote_ins)

            instructions.append((ins, host['pwd']))

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
