#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns
import os


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.init_compile_src_code <--')

        controlp_source_dir = self.getControlPSourceDir()

        ins = " && ".join([
            "free",
            "cd %s" % (os.path.join(
                controlp_source_dir, 'hadoop-maven-plugins')),
            "mvn install",
            "cd %s" % (controlp_source_dir),
            "mvn clean",
            "mvn eclipse:eclipse -DdownloadSources=true -DdownloadJavadocs=true -DskipTests",
            "mvn dependency-check:aggregate",
            # "mvn package -Pdist,native,docs,src -DskipTests -Dtar" # -Pdocs will enforce to check the format correction of docs and some mvn errors will occur.
            "mvn package -Pdist,native -DskipTests -Dtar"
        ])
        retcode = cmd.do(ins)
        if retcode != 0:
            cmd.do("mvn package -DskipTests")
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
