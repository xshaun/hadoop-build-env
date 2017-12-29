#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
import os
import shutil


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.clear_sourcecode <--')

        controlp_source_dir = self.getControlPSourceDir()

        if not os.path.exists(controlp_source_dir):
            os.makedirs(controlp_source_dir)

        if not os.path.isdir(controlp_source_dir):
            logger.error(
                '\'controlp_source_dir\' does not indicate a folder in setting file.')
            return False

        for item in os.listdir(controlp_source_dir):
            itemsrc = os.path.join(controlp_source_dir, item)
            if os.path.isdir(itemsrc):
                shutil.rmtree(itemsrc)
            else:
                os.remove(itemsrc)

        if len(os.listdir(controlp_source_dir)) > 0:
            logger.error(
                'failed to clear \'controlp_source_dir\' shown in setting file.')
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
