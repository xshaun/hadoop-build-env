#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def action(self):
        logger.info('--> controlp.download_bin_code <--')

        controlp_binary_dir = self.getControlPBinaryDir()

        if not os.path.exists(controlp_binary_dir):
            os.makedirs(controlp_binary_dir)

        if not os.path.isdir(controlp_binary_dir):
            logger.error(
                '\'binary code\' does not indicate a folder in setting file.')
            return False

        link_address = "http://www-eu.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}.tar.gz".format(
            self.ys['version'])
        ins = "curl -sSL {0} | tar -C {1} -xzv".format(
            link_address, os.path.join(controlp_binary_dir, '../'))  # TODO, only exclude files

        retcode = Command.do(ins)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
