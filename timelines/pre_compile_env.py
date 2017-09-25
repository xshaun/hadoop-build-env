#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd


class CustomEvent(BasisEvent):
    
    #override   
    def action(ys):
        # res = cmd.shell('ls ./pre.runtime')
        # print(res)
        # print(b)

        return True

def pre_compile_env(ys):
    CustomEvent(ys).run()