#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os


class Custom(Basis):

    def __parse(self, param):
        VERSION = self.ys['version']

        YARN_DIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn')
        YARN_DIR_FOR = ("%s/{0}/target/{0}-%s.jar" % (YARN_DIR, VERSION))

        YARN_SERVER_DIR = self.getControlPSourceDir(
            subdir='hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server')
        YARN_SERVER_DIR_FOR = ("%s/{0}/target/{0}-%s.jar" % (
            YARN_SERVER_DIR, VERSION))

        MAPREDUCE_CLIENT_DIR = self.getControlPSourceDir(
            subdir='hadoop-mapreduce-project/hadoop-mapreduce-client')
        MAPREDUCE_CLIENT_DIR_FOR = ("%s/{0}/target/{0}-%s.jar" % (
            MAPREDUCE_CLIENT_DIR, VERSION))

        YARN_DESTDIR = self.getClusterBinaryDir(subdir='share/hadoop/yarn/')
        MAPREDUCE_DESTDIR = self.getClusterBinaryDir(
            subdir='share/hadoop/mapreduce//')

        if 'hadoop-yarn-api' == param:  # yarn-api
            return [YARN_DIR_FOR.format('hadoop-yarn-api'), YARN_DESTDIR]

        if 'hadoop-yarn-client' == param:  # yarn-client
            return [YARN_DIR_FOR.format('hadoop-yarn-client'), YARN_DESTDIR]

        if 'hadoop-yarn-common' == param:  # yarn-common
            return [YARN_DIR_FOR.format('hadoop-yarn-common'), YARN_DESTDIR]

        if 'hadoop-yarn-registry' == param:  # yarn-registry
            return [YARN_DIR_FOR.format('hadoop-yarn-registry'), YARN_DESTDIR]

        if 'hadoop-yarn-server-common' == param:  # yarn-server-common
            return [YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-common'), YARN_DESTDIR]

        if 'ysnm' == param:  # yarn-server-nodemanager
            return [YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-nodemanager'), YARN_DESTDIR]

        if 'ysrm' == param:  # yarn-server-resourcemanager
            return [YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-resourcemanager'), YARN_DESTDIR]

        if 'hadoop-yarn-server-nodemanager' == param:  # yarn-server-nodemanager
            return [YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-nodemanager'), YARN_DESTDIR]

        if 'hadoop-yarn-server-resourcemanager' == param:  # yarn-server-resourcemanager
            return [YARN_SERVER_DIR_FOR.format('hadoop-yarn-server-resourcemanager'), YARN_DESTDIR]

        if 'hadoop-mapreduce-client-app' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-app'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-common' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-common'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-core' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-core'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-hs-plugins' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-hs-plugins'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-hs' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-hs'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-jobclient' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-jobclient'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-nativetask' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-nativetask'), MAPREDUCE_DESTDIR]

        if 'hadoop-mapreduce-client-shuffle' == param:
            return [MAPREDUCE_CLIENT_DIR_FOR.format('hadoop-mapreduce-client-shuffle'), MAPREDUCE_DESTDIR]

        # TODO, add more
        raise Exception("cannot find such param: %s" % param)
        return

    def action(self):
        logger.info('--> controlp.distribute_binary_package <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        controlp_binary_dir = self.getControlPBinaryDir()
        cluster_binary_dir = self.getClusterBinaryDir()

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
        params = self.getParams()

        instructions = list()
        if len(params) > 0:
            """
            # with params
            """
            candidates = list()

            for p in params:
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
            controlp_binary_files = os.path.join(controlp_binary_dir, '*')
            cluster_binary_files = os.path.join(cluster_binary_dir, '*')

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
