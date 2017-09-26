#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger

class CustomEvent(BasisEvent):

    #override
    def action(self):
        logger.info('--> timelines.ag.compile_prerequisites <--')

        debian_shell = '/bin/sh -c ./utility/t.switch_ali_maven.sh'
        res = cmd.do(debian_shell)
        if res != 0:
            return False

        debian_shell = '/bin/sh -c ./utility/t.pre_compile_env.sh'
        res = cmd.sudo(debian_shell, self.ys['pwds']['ag'])
        if res != 0:
            return False

        return True

def compile_prerequisites(ys):
    return CustomEvent(ys).occur(attempts=3, interval=3)
