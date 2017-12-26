#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
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

        threads = list()
        for host in host_list:
            ins = "ssh {0} {2}@{1} -tt 'sudo -S {3}'".format(
                ssh_option, host['ip'], host['usr'],
                runtime_env)

            t = ParaIns(ins, host['pwd'])
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = t.ret == ret
        return ret


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
