#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command


class Custom(Basis):

    def action(self):
        logger.info('--> controlp.init_compile_src_code <--')

        controlp_source_dir = self.getControlPSourceDir()
        controlp_source_maven_plugins_dir = self.getControlPSourceDir(
            subdir='hadoop-maven-plugins')

        ins = " && ".join([
            "free",
            "cd %s" % (controlp_source_maven_plugins_dir),
            "mvn install",
            "cd %s" % (controlp_source_dir),
            "mvn clean",
            "mvn eclipse:eclipse -DdownloadSources=true -DdownloadJavadocs=true -DskipTests",
            # "mvn dependency-check:aggregate", # TODO, fix hanging
            # "mvn package -Pdist,native,docs,src -DskipTests -Dtar" # -Pdocs will enforce to check the format correction of docs and some mvn errors will occur.
            "mvn clean install -Pdist,native -DskipTests -Dmaven.test.skip=true -Dtar"
        ])
        retcode = Command.do(ins)
        if retcode != 0:
            Command.do("mvn package -DskipTests")
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
