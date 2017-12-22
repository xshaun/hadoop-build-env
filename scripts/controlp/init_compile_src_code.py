#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.init_compile_src_code <--')

        sourcecode = self.ys['sourcecode']

        ins = " && ".join([
            "free",
            "cd %s" % (os.path.join(sourcecode, 'hadoop-maven-plugins')),
            "mvn install",
            "cd %s" % (sourcecode),
            "mvn clean",
            "mvn eclipse:eclipse -DdownloadSources=true -DdownloadJavadocs=true -DskipTests",
            "mvn dependency-check:aggregate",
            # "mvn package -Pdist,native,docs,src -DskipTests -Dtar" # -Pdocs will enforce to check the format correction of docs and some mvn errors will occur.
            "mvn package -Pdist,native,src -DskipTests"
        ])
        retcode = cmd.do(ins)
        if retcode != 0:
            cmd.do("mvn package -DskipTests")
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
