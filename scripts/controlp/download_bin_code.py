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
_version = '3.0.0-beta1'


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.download_bin_code <--')

        sourcecode = self.ys['sourcecode']

        if not os.path.exists(sourcecode):
            os.makedirs(sourcecode)

        if not os.path.isdir(sourcecode):
            logger.error(
                '\'sourcecode\' does not indicate a folder in setting file.')
            return False

        link_address = "http://www-eu.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}.tar.gz".format(
            _version)
        download = "curl -sSL {0} | tar -C {1} -xzv".format(
            link_address, sourcecode)
        movedir = "mkdir -p {0} && mv {1}/* {0} && rmdir {1} ".format(
            os.path.join(sourcecode, "hadoop-dist/target/hadoop-%s" %
                         (_version)),
            os.path.join(sourcecode, "hadoop-%s" % (_version)))

        ins = "%s && %s" % (download, movedir)
        retcode = cmd.do(ins)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
