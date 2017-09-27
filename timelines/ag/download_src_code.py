#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
# _version indicates downloading binary code version
#
_version = '3.0.0-alpha4'

class CustomEvent(BasisEvent):

    #override
    def action(self):
        logger.info('--> timelines.ag.download_src_code <--')

        codefolder = self.ys['codepath']

        if not os.path.exists(codefolder):
            os.makedirs(codefolder)

        if not os.path.isdir(codefolder):
            logger.error('\'codepath\' does not indicate a folder in setting file.')
            return False

        linkaddress = "http://www-eu.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}-src.tar.gz".format(_version)
        shell = "curl -sSL {0} | tar -C {1} -xzv".format(linkaddress, codefolder)
        
        retcode = cmd.do(shell)
        if retcode != 0:
            return False

        return True

def download_src_code(ys):
    return CustomEvent(ys).occur(attempts=3, interval=3)
