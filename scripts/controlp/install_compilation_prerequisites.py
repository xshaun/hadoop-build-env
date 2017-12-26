#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.install_compilation_prerequisites <--')

        ins = './utilities/setup_aliyun_maven_mirror.sh'
        retcode = cmd.do(ins)
        if retcode != 0:
            return False

        ins = 'sudo -S ./utilities/install_compilation_prerequisites.sh'
        retcode = cmd.sudo(ins, self.ys['roles']['controlp']['pwd'])
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
