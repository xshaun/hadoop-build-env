#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger
import os


class CustomEvent(BasisEvent):

    # override
    def action(self):
        logger.info('--> timelines.ag.compile_src_code <--')

        codefolder = self.ys['codepath']

        _maven_shell = " && ".join([
            "cd %s" % (os.path.join(codefolder, 'hadoop-maven-plugins')),
            "mvn install",
            "cd %s" % (codefolder),
            "mvn clean",
            "mvn eclipse:eclipse -DdownloadSources=true -DdownloadJavadocs=true -DskipTests",
            "mvn dependency-check:aggregate",
            "mvn package -Pdist,native,docs,src -DskipTests -Dtar"
        ])
        retcode = cmd.do(_maven_shell)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = CustomEvent(ys, attempts=5, interval=10, auto=True)
    return e.status
