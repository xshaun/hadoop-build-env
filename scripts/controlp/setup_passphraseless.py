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
        logger.info('--> controlp.setup_passphraseless <--')

        host_list = self.getHosts()

        threads = list()

        for host in host_list:
            # setup passphraseless
            ins = "./utilities/setup_passphraseless.sh '%s@%s' '%s'" % (
                host['usr'], host['ip'], host['pwd'])

            t = ParaIns(ins)
            t.start()
            threads.append(t)

        # wait
        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = t.ret == ret
        return ret


def trigger(ys):
    e = Custom(ys, attempts=5, interval=3, auto=True)
    return e.status
