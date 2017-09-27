#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger
import os

class CustomEvent(BasisEvent):

    #override
    def action(self):
        logger.info('--> timelines.ag.compile_src_code <--')

        folder = self.ys['codepath']

        maven_shell = "cd {0} && mvn install \
            && cd {1} \
            && mvn clean \
            && mvn eclipse:eclipse -DskipTests \
            && mvn dependency-check:aggregate \
            && mvn package -Pdist,native,docs,src -DskipTests -Dtar" % (
                os.path.join(folder, 'hadoop-maven-plugins'), folder)

        res = cmd.do(maven_shell)
        if res != 0:
            return False

        return True

def compile_src_code(ys):
    return CustomEvent(ys).occur(attempts=5, interval=10)