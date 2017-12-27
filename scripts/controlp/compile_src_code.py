#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
from scripts.command import ParaIns
import os


class Custom(Basis):

    def __parse(self, param):
        if 'yapi' == param:  # yarn-api
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-api/')

        if 'yclient' == param:  # yarn-client
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-client/')

        if 'ycommon' == param:  # yarn-common
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-common/')

        if 'yscommon' == param:  # yarn-server-common
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-common/')

        if 'ysnm' == param:  # yarn-server-nodemanager
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-nodemanager/')

        if 'ysrm' == param:  # yarn-server-resourcemanager
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager/')

        # TODO, add more
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

        threads = list()
        for can in candidates:
            ins = " && ".join([
                "cd %s" % (can),
                # "mvn package -Pdist,native,docs,src -DskipTests -Dtar" # -Pdocs will enforce to check the format correction of docs and some mvn errors will occur.
                # "mvn package -Pdist,native,src -T 1C -Dmaven.test.skip=true  -Dmaven.compile.fork=true"
                "mvn clean && mvn install -Pdist,native -DskipTests -Dtar"
            ])

            t = ParaIns(ins)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = t.ret == ret
        return ret


def trigger(ys, params=[]):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
