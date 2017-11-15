#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
# _version indicates downloading binary code version
#
_version = '3.0.0-alpha4'


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.download_bin_code <--')

        codefolder = self.ys['codefolder']

        if not os.path.exists(codefolder):
            os.makedirs(codefolder)

        if not os.path.isdir(codefolder):
            logger.error(
                '\'codefolder\' does not indicate a folder in setting file.')
            return False

        link_address = "http://www-eu.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}.tar.gz".format(
            _version)
        download = "curl -sSL {0} | tar -C {1} -xzv".format(
            link_address, codefolder)
        movedir = "mv {0}/* {1} && rmdir {0} ".format(
            os.path.join(codefolder, "hadoop-%s" % (_version)), codefolder)

        ins = "%s && %s" % (download, movedir)
        retcode = cmd.do(ins)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
