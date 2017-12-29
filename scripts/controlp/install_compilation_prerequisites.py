#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command


class Custom(Basis):

    def action(self):
        logger.info('--> controlp.install_compilation_prerequisites <--')

        ins = './utilities/setup_aliyun_maven_mirror.sh'
        retcode = Command.do(ins)
        if retcode != 0:
            return False

        ins = 'sudo -S ./utilities/install_compilation_prerequisites.sh'
        retcode = Command.sudo(ins, self.ys['roles']['controlp']['pwd'])
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
