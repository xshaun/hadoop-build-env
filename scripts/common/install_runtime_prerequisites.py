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

        usr_host_list = list()

        roles_without_controller = dict(filter(lambda x: x[0] != 'controlp',
            self.ys['roles'].items()))
        for k, v in roles_without_controller.items():
            usr_host_list.extend([ v['usr'] + '@' + n for n in v['hosts'] ])

        usr_host_list = list(set(usr_host_list))

        #
        # build master and slaves environment
        #
        # TODO [support to parallel execution]
        slave_scripts_folder = os.path.join(self.ys['binarycode'], 'scripts/')
        remote_ins = "sudo -S %s/install_runtime_prerequisites.sh" % (slave_scripts_folder)

        for k, v in roles_without_controller.items():
            for host in v['hosts']:
                usr_host = (v['usr']+'@'+host)

                if usr_host in usr_host_list:
                    usr_host_list.remove(usr_host)

                    ins = "{0} {1} -tt '{2}' ".format(
                            ssh_option, usr_host, remote_ins)
                    retcode = cmd.sudo(ins, v['pwd'])
                    logger.info("ins: %s; retcode: %d." % (ins, retcode))

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
