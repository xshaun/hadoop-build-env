#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.distribute_binary_package_prep <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        cluster_script_dir = self.getClusterScriptDir()
        cluster_binary_dir = self.getClusterBinaryDir()

        #
        # add permissions
        # -------------------------------------------------------
        #
        ret = True
        instructions = list()
        for host in host_list:
            """
            create folders
            """
            ins = "ssh {0} {2}@{1} -tt 'sudo -S mkdir -p {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            instructions.append((ins, host['pwd']))

        ret = ret == Command.parallel(instructions)

        instructions = list()
        for host in host_list:
            """
            chown
            """
            ins = "ssh {0} {2}@{1} -tt 'sudo -S chown -R {2} {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            instructions.append((ins, host['pwd']))

        ret = ret == Command.parallel(instructions)

        instructions = list()
        for host in host_list:
            """
            chmod
            """
            ins = "ssh {0} {2}@{1} -tt 'sudo -S chmod -R 777 {3}' ".format(
                ssh_option, host['ip'], host['usr'], cluster_binary_dir)

            instructions.append((ins, host['pwd']))

        ret = ret == Command.parallel(instructions)
        if not ret:
            return ret

        #
        # create hdfs folders
        # -------------------------------------------------------
        #
        instructions = list()

        """ folders for namenode """
        name_nodes = self.getHosts(roles=['namen', ])

        namedir = self.getClusterHdfsDir(
            subdir=self.ys['roles']['namen']['dir'])

        namesdir = self.getClusterHdfsDir(
            subdir=self.ys['roles']['namen']['sdir'])

        for host in name_nodes:
            ins = "ssh {0} {2}@{1} -tt 'mkdir -p {3} {4}' ".format(
                ssh_option, host['ip'], host['usr'], namedir, namesdir)

            instructions.append(ins)

        """ folders for datanodes """
        data_nodes = self.getHosts(roles=['datan', ])

        datadir = self.getClusterHdfsDir(
            subdir=self.ys['roles']['datan']['dir'])

        for host in data_nodes:
            ins = "ssh {0} {2}@{1} -tt 'mkdir -p {3}' ".format(
                ssh_option, host['ip'], host['usr'], datadir)

            instructions.append(ins)

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        #
        # scripts about building env
        # -------------------------------------------------------
        #
        instructions = list()

        hbe_utilities = './utilities/*'

        for host in host_list:
            ins = ("ssh {0} {2}@{1} -tt 'mkdir -p {4}' "
                   "&& scp -r {0} {3} {2}@{1}:{4} ").format(
                ssh_option, host['ip'], host['usr'],
                hbe_utilities, cluster_script_dir)

            instructions.append(ins)

        ret = Command.parallel(instructions)
        if not ret:
            return ret

        #
        # config setup_passphraseless from master to slaves
        # -------------------------------------------------------
        #
        instructions = list()

        setup_passphraseless = os.path.join(
            cluster_script_dir, 'setup_passphraseless.sh')

        # hdfs
        namenode = self.getHosts(roles=['namen', ])
        datanodes = self.getHosts(roles=['datan', ])

        datanodes_hostname = list()
        for host in datanodes:
            datanodes_hostname.append("%s@%s" % (host['usr'], host['ip']))

        for host in namenode:
            ins = "ssh {0} {2}@{1} -tt '{3} \'{4}\' \'{5}\'' ".format(
                ssh_option, host['ip'], host['usr'],
                setup_passphraseless, ",".join(datanodes_hostname),
                self.ys['roles']['datan']['pwd'])

            instructions.append(ins)

        # yarn
        resourcemanager = self.getHosts(roles=['resourcem', ])
        nodemanagers = self.getHosts(roles=['nodem', ])

        nodemanagers_hostname = list()
        for host in nodemanagers:
            nodemanagers_hostname.append("%s@%s" % (host['usr'], host['ip']))

        for host in resourcemanager:
            ins = "ssh {0} {2}@{1} -tt '{3} \'{4}\' \'{5}\''".format(
                ssh_option, host['ip'], host['usr'],
                setup_passphraseless, ",".join(nodemanagers_hostname),
                self.ys['roles']['nodem']['pwd'])

            instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
