#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger

class CustomEvent(BasisEvent):

    #override
    def action(self):
        logger.info('--> timelines.ag.clear_codepath <--')

        folder = ys['codepath']

        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.isdir(folder):
            logger.error('\'codepath\' does not indicate a folder in setting file.')
            return False

        for item in os.listdir(folder):  
            itemsrc = os.path.join(folder, item)
            if os.path.isdir(itemsrc):
                __import__('shutil').rmtree(itemsrc)
            else:
                os.remove(itemsrc)

        if len(os.listdir(folder)) > 0 :
            logger.error('failed to clear \'codepath\' shown in setting file.')
            return False

        return True

def clear_codepath(ys):
    return CustomEvent(ys).occur(attempts=3, interval=3)
