#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
from random import choice
import os


class Custom(Basis):

    def action(self):
        logger.info('--> common.submit <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        slaves_list = self.getSlaveHosts()

        instructions = list()
        for p in self.ys['params']:
            host = choice(slaves_list)

            #!!! donot use -tt option
            ins = "ssh {0} {2}@{1} -T 'cd {3} && {4}' ".format(
                ssh_option, host['ip'], host['usr'],
                self.getClusterBinaryDir(), p)

            instructions.append(ins)

        return Command.parallel(instructions)

def trigger(ys):
    e = Custom(ys, attempts=1, interval=30, auto=True)
    return e.status
