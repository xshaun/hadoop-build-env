#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger

class CustomEvent(BasisEvent):

    #override
    def action(self):
        logger.info('--> timelines.pre_compile_env <--')

        debian_shell = '/bin/sh -c ./t.pre_compile_env.sh'

        res = cmd.sudo(debian_shell, self.ys['pwds']['ag'])
        if res != 0:
            return False
        return True

def pre_compile_env(ys):
    return CustomEvent(ys).occur(attempts=3, interval=3)
