#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.setup_passphraseless <--')

        host_list = self.getHosts()

        instructions = list()
        for host in host_list:
            # setup passphraseless
            ins = "./utilities/setup_passphraseless.sh '%s@%s' '%s'" % (
                host['usr'], host['ip'], host['pwd'])
            instructions.append(ins)

        return Command.parallel(ins_list)


def trigger(ys):
    e = Custom(ys, attempts=5, interval=3, auto=True)
    return e.status
