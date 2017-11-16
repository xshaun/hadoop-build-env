#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.setup_passphraseless <--')

        # setup passphraseless
        roles_without_controller = dict(filter(lambda x: x[0] != 'controlp',
            self.ys['roles'].items()))
 
        for k, v in roles_without_controller.items():
            usr_host_list = list(set([ v['usr'] + '@' + n for n in v['hosts'] ]))

            ins = "./utilities/setup_passphraseless.sh %s %s" % (
                ','.join(usr_host_list), v['pwd'])
            retcode = cmd.do(ins)
            if retcode != 0:
                return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
