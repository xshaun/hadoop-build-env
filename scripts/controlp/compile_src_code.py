#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.compile_src_code <--')

        codefolder = self.ys['codefolder']

        ins = " && ".join([
            "cd %s" % (os.path.join(codefolder, 'hadoop-maven-plugins')),
            "mvn install",
            "cd %s" % (codefolder),
            "mvn clean",
            "mvn eclipse:eclipse -DdownloadSources=true -DdownloadJavadocs=true -DskipTests",
            "mvn dependency-check:aggregate",
            "mvn package -Pdist,native,docs,src -DskipTests -Dtar"
        ])
        retcode = cmd.do(ins)
        if retcode != 0:
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
