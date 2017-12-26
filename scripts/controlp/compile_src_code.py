#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os


class Custom(Basis):

    def __parse(self, param):
        if param is 'nm':
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-nodemanager/')

        if param is 'rm':
            return os.path.join(self.getControlPSourceDir(),
                                'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager')

        # TODO, add more
        return

    # override
    def action(self):
        logger.info('--> controlp.compile_src_code <--')

        controlp_source_dir = self.getControlPSourceDir()

        candidates = list()

        if len(self.ys['params']) == 0:
            candidates.append(controlp_source_dir)
        else:
            for p in self.ys['params']:
                candidates.append(self.__parse(p))

        threads = list()
        for can in candidates:
            ins = " && ".join([
                "cd %s" % (can),
                # "mvn package -Pdist,native,docs,src -DskipTests -Dtar" # -Pdocs will enforce to check the format correction of docs and some mvn errors will occur.
                # "mvn package -Pdist,native,src -T 1C -Dmaven.test.skip=true  -Dmaven.compile.fork=true"
                "mvn clean && mvn package -Pdist,native -DskipTests -Dtar"
            ])

            t = ParaIns(ins)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = ret and t.ret
        return ret


def trigger(ys, params=[]):
    e = Custom(ys, attempts=5, interval=10, auto=True)
    return e.status
