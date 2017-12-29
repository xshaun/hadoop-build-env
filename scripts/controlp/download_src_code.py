#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.download_src_code <--')

        controlp_source_dir = self.getControlPSourceDir()

        if not os.path.exists(controlp_source_dir):
            os.makedirs(controlp_source_dir)

        if not os.path.isdir(controlp_source_dir):
            logger.error(
                '\'source code\' does not indicate a folder in setting file.')
            return False

        link_address = "http://www-eu.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}-src.tar.gz".format(
            self.ys['version'])
        ins = "curl -sSL {0} | tar -C {1} -xzv".format(
            link_address, os.path.join(controlp_source_dir, '../')) # TODO, only exclude files

        retcode = Command.do(ins)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
