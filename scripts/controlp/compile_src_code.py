#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command


class Custom(Basis):

    def __parse(self, param):
        YARNDIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn')
        YARNDIRFOR = "%s/{0}" % (YARNDIR)

        YARNSERVERDIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server')
        YARNSERVERDIRFOR = "%s/{0}" % (YARNSERVERDIR)

        if 'yapi' == param:  # yarn-api
            return YARNDIRFOR.format('hadoop-yarn-api')

        if 'yclient' == param:  # yarn-client
            return YARNDIRFOR.format('hadoop-yarn-client')

        if 'yregistry' == param:  # yarn-registry
            return YARNDIRFOR.format('hadoop-yarn-registry')

        if 'ycommon' == param:  # yarn-common
            return YARNDIRFOR.format('hadoop-yarn-common')

        if 'yscommon' == param:  # yarn-server-common
            return YARNSERVERDIRFOR.formta('hadoop-yarn-server-common')

        if 'ysnm' == param:  # yarn-server-nodemanager
            return YARNSERVERDIRFOR.formta('hadoop-yarn-server-nodemanager')

        if 'ysrm' == param:  # yarn-server-resourcemanager
            return YARNSERVERDIRFOR.formta('hadoop-yarn-server-resourcemanager')

        # TODO, add more
        raise Exception("cannot find such param: %s" % param)
        return

    # override
    def action(self):
        logger.info('--> controlp.compile_src_code <--')

        controlp_source_dir = self.getControlPSourceDir()

        candidates = list()
        for p in self.ys['params']:
            candidates.append(self.__parse(p))

        if len(candidates) == 0:
            candidates.append(controlp_source_dir)

        instructions = list()
        for can in candidates:
            ins = " && ".join([
                "cd %s" % (can),
                "mvn clean install -Pdist,native -DskipTests -Dtar"
            ])

            instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys, params=[]):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
