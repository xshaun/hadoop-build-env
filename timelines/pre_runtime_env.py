#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd

class CustomEvent(BasisEvent):

    #override
    def action(ys):
        debian_shell = './t.pre_runtime_env.sh'

        res = cmd.sudo(debian_shell, 'xboy')
        if res != 0:
            return False
        return True

def pre_runtime_env(ys):
    return CustomEvent(ys).occur(attempts=3, interval=3)


