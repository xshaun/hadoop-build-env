#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def __parse(self, param):
        VERSION = self.ys['version']

        YARNDIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn')
        YARNDIRFOR = ("%s/{0}/target/{0}-%s.jar" % (YARNDIR, VERSION))

        YARNSERVERDIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server')
        YARNSERVERDIRFOR = ("%s/{0}/target/{0}-%s.jar" % (
            YARNSERVERDIR, VERSION))

        DESTDIR = self.getClusterBinaryDir(subdir='share/hadoop/yarn/')

        if 'yapi' == param:  # yarn-api
            return [YARNDIRFOR.format('hadoop-yarn-api'), DESTDIR]

        if 'yclient' == param:  # yarn-client
            return [YARNDIRFOR.format('hadoop-yarn-client'), DESTDIR]

        if 'ycommon' == param:  # yarn-common
            return [YARNDIRFOR.format('hadoop-yarn-common'), DESTDIR]

        if 'yregistry' == param:  # yarn-registry
            return [YARNDIRFOR.format('hadoop-yarn-registry'), DESTDIR]

        if 'yscommon' == param:  # yarn-server-common
            return [YARNSERVERDIRFOR.format('hadoop-yarn-server-common'), DESTDIR]

        if 'ysnm' == param:  # yarn-server-nodemanager
            return [YARNSERVERDIRFOR.format('hadoop-yarn-server-nodemanager'), DESTDIR]

        if 'ysrm' == param:  # yarn-server-resourcemanager
            return [YARNSERVERDIRFOR.format('hadoop-yarn-server-resourcemanager'), DESTDIR]

        # TODO, add more
        raise Exception("cannot find such param: %s" % param)
        return

    def action(self):
        logger.info('--> controlp.distribute_binary_package <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        """ chmod """
        instructions = list()
        for host in host_list:
            ins = "ssh {0} {2}@{1} -tt 'sudo -S chmod -R 777 {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            instructions.append((ins, host['pwd']))

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        """ sync binary files """
        instructions = list()
        if len(self.ys['params']) > 0:
            """
            # with params
            """
            candidates = list()

            for p in self.ys['params']:
                candidates.append(self.__parse(p))

            for can in candidates:
                for host in host_list:
                    ins = ("scp -r {0} {3} {2}@{1}:{4}").format(
                        ssh_option, host['ip'], host['usr'],
                        can[0], can[1])

                    instructions.append(ins)
        else:
            """
            # without params
            """
            controlp_binary_dir = self.getControlPBinaryDir()
            cluster_binary_dir = self.getClusterBinaryDir()
            controlp_binary_files = os.path.join(controlp_binary_dir, '*')
            cluster_binary_files = os.path.join(cluster_binary_dir, '*')
            cluster_hadoop_conf_dir = self.getClusterHadoopConfDir()

            for host in host_list:
                ins = ("ssh {0} {2}@{1} -tt 'mkdir -p {4} && rm -rf {5}'"
                       " && scp -r {0} {3} {2}@{1}:{4}").format(
                    ssh_option, host['ip'], host['usr'],
                    controlp_binary_files, cluster_binary_dir, cluster_binary_files)

                instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
