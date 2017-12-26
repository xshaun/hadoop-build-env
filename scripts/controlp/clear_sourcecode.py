#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os
import shutil


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.clear_sourcecode <--')

        sourcecode = self.getControlPSourceDir()

        if not os.path.exists(sourcecode):
            os.makedirs(sourcecode)

        if not os.path.isdir(sourcecode):
            logger.error(
                '\'sourcecode\' does not indicate a folder in setting file.')
            return False

        for item in os.listdir(sourcecode):
            itemsrc = os.path.join(sourcecode, item)
            if os.path.isdir(itemsrc):
                shutil.rmtree(itemsrc)
            else:
                os.remove(itemsrc)

        if len(os.listdir(sourcecode)) > 0:
            logger.error(
                'failed to clear \'sourcecode\' shown in setting file.')
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
