#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command as cmd
import os

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------


class Custom(Basis):

    # override
    def action(self):
        logger.info('--> controlp.distribute_binary_package<--')

        ssh_option = 'ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5'

        host_list = self.getHosts()

        sourcecode = self.ys['sourcecode']
        binarycode = self.ys['binarycode']

        #
        # add permissions
        #
        for host in host_list:
            """
            create folders
            """
            ins = "{0} {2}@{1} -tt 'sudo -S mkdir -p {3}' ".format(
                ssh_option, host['ip'], host['usr'], binarycode)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

            """
            chown
            """
            ins = "{0} {2}@{1} -tt 'sudo -S chown -R {2} {3}' ".format(
                ssh_option, host['ip'], host['usr'], binarycode)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

            """
            chmod
            """
            ins = "{0} {2}@{1} -tt 'sudo -S chmod -R 777 {3}' ".format(
                ssh_option, host['ip'], host['usr'], binarycode)

            retcode = cmd.sudo(ins, host['pwd'])

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # create hdfs folders
        #

        """
        folders for namenode
        """
        name_nodes = self.getHosts(roles=['namen', ])

        namedir = os.path.join(binarycode, self.ys['roles']['namen']['dir'])
        namesdir = os.path.join(binarycode, self.ys['roles']['namen']['sdir'])

        for host in name_nodes:
            ins = "{0} {2}@{1} -tt 'mkdir -p {3} {4}' & sleep 0.5".format(
                ssh_option, host['ip'], host['usr'],
                namedir, namesdir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        """
        folders for datanodes
        """
        data_nodes = self.getHosts(roles=['datan', ])

        datadir = os.path.join(binarycode, self.ys['roles']['datan']['dir'])

        for host in data_nodes:
            ins = "{0} {2}@{1} -tt 'mkdir -p {3}' & sleep 0.5".format(
                ssh_option, host['ip'], host['usr'],
                datadir)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # binary code
        #
        sour_folder = os.path.join(
            sourcecode, 'hadoop-dist/target/hadoop-3.0.0-beta1/')
        dest_folder = os.path.join(binarycode, 'rose-on-yarn/')

        for host in host_list:
            ins = "{0} {2}@{1} -tt 'mkdir -p {4}' && rsync -e '{0}' -az '{3}' {2}@{1}:{4} & sleep 0.5".format(
                ssh_option, host['ip'], host['usr'],
                sour_folder, dest_folder)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # scripts about building env
        #
        controlp_scripts = './utilities/'
        dest_scripts_folder = os.path.join(binarycode, 'scripts/')

        for host in host_list:
            ins = "{0} {2}@{1} -tt 'mkdir -p {4}' && rsync -e '{0}' -az '{3}' {2}@{1}:{4} & sleep 0.5".format(
                ssh_option, host['ip'], host['usr'],
                controlp_scripts, dest_scripts_folder)

            retcode = cmd.do(ins)

            logger.info("ins: %s; retcode: %d." % (ins, retcode))

            if retcode != 0:
                logger.error(ins)
                return False

        #
        # config setup_passphraseless from master to slaves
        #
        master_hosts_list = self.getMasterHosts()
        slave_hosts_list = self.getSlaveHosts()
        setup_passphraseless = os.path.join(
            dest_scripts_folder, 'setup_passphraseless.sh')

        for mhost in master_hosts_list:
            for shost in slave_hosts_list:
                ins = "{0} {2}@{1} -tt '{3} {5}@{4} {6}' & sleep 0.5".format(
                    ssh_option, mhost['ip'], mhost['usr'],
                    setup_passphraseless, shost['ip'], shost['usr'], shost['pwd'])

                retcode = cmd.do(ins)

                logger.info("ins: %s; retcode: %d." % (ins, retcode))

                if retcode != 0:
                    logger.error(ins)
                    return False

        #
        # configs
        #
        controlp_configs = './configs/*.xml ./configs/workers'
        dest_configs_folder = os.path.join(
            binarycode, 'rose-on-yarn/etc/hadoop/')

        for host in host_list:
            ins = "scp {0} {2}@{1}:{3} & sleep 0.5".format(
                controlp_configs, host['ip'], host['usr'],
                dest_configs_folder)

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
