#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger
import os, shutil

class CustomEvent(BasisEvent):

    #override
    def action(self):
        logger.info('--> timelines.ag.clear_codepath <--')

        codefolder = self.ys['codepath']

        if not os.path.exists(codefolder):
            os.makedirs(codefolder)

        if not os.path.isdir(codefolder):
            logger.error('\'codepath\' does not indicate a folder in setting file.')
            return False

        for item in os.listdir(codefolder):  
            itemsrc = os.path.join(codefolder, item)
            if os.path.isdir(itemsrc):
                shutil.rmtree(itemsrc)
            else:
                os.remove(itemsrc)

        if len(os.listdir(codefolder)) > 0 :
            logger.error('failed to clear \'codepath\' shown in setting file.')
            return False

        return True

def clear_codepath(ys):
    return CustomEvent(ys).occur(attempts=3, interval=3)
