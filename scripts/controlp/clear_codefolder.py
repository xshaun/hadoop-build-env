#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os
import shutil


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.clear_codefolder <--')

        codefolder = self.ys['codefolder']

        if not os.path.exists(codefolder):
            os.makedirs(codefolder)

        if not os.path.isdir(codefolder):
            logger.error(
                '\'codefolder\' does not indicate a folder in setting file.')
            return False

        for item in os.listdir(codefolder):
            itemsrc = os.path.join(codefolder, item)
            if os.path.isdir(itemsrc):
                shutil.rmtree(itemsrc)
            else:
                os.remove(itemsrc)

        if len(os.listdir(codefolder)) > 0:
            logger.error('failed to clear \'codefolder\' shown in setting file.')
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
