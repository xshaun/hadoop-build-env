#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command


class Custom(Basis):

    def __parse(self, param):
        YARN_DIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn')
        YARN_DIR_FOR = "%s/{0}" % (YARN_DIR)

        YARN_SERVER_DIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server')
        YARN_SERVER_DIR_FOR = "%s/{0}" % (YARN_SERVER_DIR)

        MAPREDUCE_CLIENT_DIR = self.getControlPSourceDir(
            subdir='hadoop-mapreduce-project/hadoop-mapreduce-client')
        MAPREDUCE_CLIENT_DIR_FOR = "%s/{0}" % (MAPREDUCE_CLIENT_DIR)

        if 'hadoop-yarn-api' == param:  # yarn-api
            return YARN_DIR_FOR.format('hadoop-yarn-api')

        if 'hadoop-yarn-client' == param:  # yarn-client
            return YARN_DIR_FOR.format('hadoop-yarn-client')

        if 'hadoop-yarn-registry' == param:  # yarn-registry
            return YARN_DIR_FOR.format('hadoop-yarn-registry')

        if 'hadoop-yarn-common' == param:  # yarn-common
            return YARN_DIR_FOR.format('hadoop-yarn-common')

        if 'hadoop-yarn-server-common' == param:  # yarn-server-common
            return YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-common')

        if 'ysnm' == param:  # yarn-server-nodemanager
            return YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-nodemanager')

        if 'ysrm' == param:  # yarn-server-resourcemanager
            return YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-resourcemanager')

        if 'hadoop-mapreduce-client-app' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-app')

        if 'hadoop-mapreduce-client-common' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-common')

        if 'hadoop-mapreduce-client-core' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-core')

        if 'hadoop-mapreduce-client-hs-plugins' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-hs-plugins')

        if 'hadoop-mapreduce-client-hs' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-hs')

        if 'hadoop-mapreduce-client-jobclient' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-jobclient')

        if 'hadoop-mapreduce-client-nativetask' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-nativetask')

        if 'hadoop-mapreduce-client-shuffle' == param:
            return MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-shuffle')

        # TODO, add more
        raise Exception("cannot find such param: %s" % param)
        return

    def action(self):
        logger.info('--> controlp.compile_src_code <--')

        controlp_source_dir = self.getControlPSourceDir()

        params = self.getParams()

        candidates = list()
        for p in params:
            candidates.append(self.__parse(p))

        if len(candidates) == 0:
            candidates.append(controlp_source_dir)

        instructions = list()
        for can in candidates:
            ins = " && ".join([
                "cd %s" % (can),
                "mvn clean install -Pdist,native -DskipTests -Dmaven.javadoc.skip=true -Dtar"
            ])

            instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys, params=[]):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
