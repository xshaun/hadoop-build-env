#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    def __parse(self, param):
        # TODO: hard code version
        if param is 'nm':
            return [os.path.join(self.getControlPSourceDir(),
                                 'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-nodemanager/',
                                 'target/hadoop-yarn-server-nodemanager-3.0.0-beta1.jar'),
                    os.path.join(self.getClusterBinaryDir(),
                                 'share/hadoop/yarn/')
                    ]

        if param is 'rm':
            return [os.path.join(self.getControlPSourceDir(),
                                 'hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager',
                                 'target/hadoop-yarn-server-resourcemanager-3.0.0-beta1.jar'),
                    os.path.join(self.getClusterBinaryDir(),
                                 'share/hadoop/yarn/')
                    ]

        # TODO, add more
        return

    # override
    def action(self):
        logger.info('--> controlp.distribute_binary_package <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        if len(self.ys['params']) != 0:
            for p in self.ys['params']:

                file = self.__parse(p)

                for host in host_list:
                    ins = ("scp -r {0} {3} {2}@{1}:{4}").format(
                        ssh_option, host['ip'], host['usr'],
                        file[0], file[1])

                    retcode = cmd.do(ins)

                    logger.info("ins: %s; retcode: %d." % (ins, retcode))

                    if retcode != 0:
                        logger.error(ins)
                        return False
            return True

        #

        controlp_binary_dir = self.getControlPBinaryDir()
        cluster_binary_dir = self.getClusterBinaryDir()
        controlp_binary_files = os.path.join(controlp_binary_dir, '*')
        cluster_binary_files = os.path.join(cluster_binary_dir, '*')
        cluster_hadoop_conf_dir = self.getClusterHadoopConfDir()

        #
        # binary code
        #
        for host in host_list:
            ins = ("ssh {0} {2}@{1} -tt 'mkdir -p {4} && rm -rf {5}'"
                   " && scp -r {0} {3} {2}@{1}:{4}").format(
                ssh_option, host['ip'], host['usr'],
                controlp_binary_files, cluster_binary_dir, cluster_binary_files)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # configs
        #
        hbe_configs = './configs/*.xml ./configs/workers'

        for host in host_list:
            ins = "scp -r {0} {3} {2}@{1}:{3} ".format(
                ssh_option, host['ip'], host['usr'],
                hbe_configs, cluster_hadoop_conf_dir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # wait to end
        #
        ins = 'wait'
        retcode = cmd.do(ins)
        if retcode != 0:
            logger.error(ins)
            return False

        return True


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
