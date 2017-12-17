#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> common.install_runtime_prerequisties <--')

        ssh_option = 'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        #
        # build master and slaves environment
        #
        # TODO [support to parallel execution]
        dest_scripts_folder = os.path.join(self.ys['binarycode'], 'scripts/')

        runtime_env = os.path.join(
            dest_scripts_folder, 'install_runtime_prerequisites.sh')

        for host in host_list:
            ins = "{0} {2}@{1} -tt 'sudo -S {3}'".format(
                ssh_option, host['ip'], host['usr'],
                runtime_env)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # wait to end
        #
        ins = 'wait'
        retcode = cmd.do(ins)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
