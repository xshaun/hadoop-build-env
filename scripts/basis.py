#!/usr/bin/env python3

import copy
import time
import os
import logging
import logging.config

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
# _logging_config is used to configue logging
# _logging_logger is used to get a logger
#
_logging_config = './configs/logging.config'
_logging_logger = 'develop'

#---------------------------------------------------------------------------
#   Core Logic
#---------------------------------------------------------------------------

logging.config.fileConfig(_logging_config)
logger = logging.getLogger(_logging_logger)


class Basis(object):
    """
    @attributes:
        - ys: settting yaml file
        - attempts: times trying to do
        - interval: pause time while failed to run
    """

    def __init__(self, ys, attempts=5, interval=5, auto=True):
        self.ys = ys
        self.attempts = attempts
        self.interval = interval  # seconds
        # TODO support status machine
        self.status = False

        if auto:  # automatically occur
            self.occur()

    def action(self):
        """ must be override, must return True or False """

        return True

    def finite(self):
        """ try to run several times despite failed """
        for x_x in range(self.attempts):
            if self.action():
                return True
            logger.info("!'o'! a failed attempt at %d-th running" % (x_x + 1))
            time.sleep(self.interval)

        return False

    def loop(self):
        """ try to run until succeed """
        while not self.action():
            logger.info('A failed attempt and tring once more until success')
            time.sleep(self.interval)

        return True

    def once(self):
        """ try to run once despite failed """
        self.attempts = 1

        return self.finite()

    def occur(self):
        """ default runtime as finite method with 5 attempts"""
        if self.attempts < 0:
            self.status = self.loop()
        else:
            self.status = self.finite()

        logger.info("--> one step is end. status is %s <--" % self.status)
        return

    def getParams(self):
        params = copy.deepcopy(self.ys['params'])
        if params is None:
            params = []

        return params

    def getHosts(self, roles=['resourcem', 'nodem', 'namen', 'datan']):
        """
         -> resource manager
         -> node manager
         -> name node
         -> data node

        return value format
        [
            [host-ip1, username1, password1]
            [host-ip2, username2, password2]
            ......
        ]
        """
        res = list()
        res_flag = list()

        roles_without_controller = dict(filter(lambda x: x[0] in roles,
                                               self.ys['roles'].items()))
        for k, v in roles_without_controller.items():
            for h in v['hosts']:
                t = "%s-%s-%s" % (h, v['usr'], v['pwd'])
                if t not in res_flag:
                    res.append({'ip': h, 'usr': v['usr'], 'pwd': v['pwd']})
                    res_flag.append(t)

        return copy.deepcopy(res)

    def getMasterHosts(self):
        """
         -> resource manager
         -> name node

        return value format
        [
            [host-ip1, username1, password1]
            [host-ip2, username2, password2]
            ......
        ]
        """
        return self.getHosts(roles=['resourcem', 'namen'])

    def getSlaveHosts(self):
        """
         -> node manager
         -> data node

        return value format
        [
            [host-ip1, username1, password1]
            [host-ip2, username2, password2]
            ......
        ]
        """
        return self.getHosts(roles=['nodem', 'datan'])

    """
    Functions: get*Dir
    """

    def getControlPSourceDir(self, subdir=''):

        return os.path.join(self.ys['controlp_base_path'],
                            subdir)

    def getControlPBinaryDir(self, subdir=''):

        return self.getControlPSourceDir(subdir=os.path.join(
            "hadoop-dist/target/hadoop-%s" % self.ys['version'], subdir))

    def getClusterBaseDir(self, subdir=''):

        return os.path.join(self.ys['cluster_base_path'],
                            subdir)

    def getClusterScriptDir(self, subdir=''):

        return self.getClusterBaseDir(subdir=os.path.join(
            'scripts', subdir))

    def getClusterBinaryDir(self, subdir=''):

        return self.getClusterBaseDir(subdir=os.path.join(
            'rose-on-yarn', subdir))

    def getClusterLogDir(self, subdir=''):

        return self.getClusterBaseDir(subdir=os.path.join(
            'logs', subdir))

    def getClusterTmpDir(self, subdir=''):
        return self.getClusterBaseDir(subdir=os.path.join(
            'tmp', subdir))

    def getClusterHdfsDir(self, subdir=''):

        return self.getClusterBaseDir(subdir=os.path.join(
            'hdfs', subdir))

    def getClusterHadoopConfDir(self, subdir=''):

        return self.getClusterBinaryDir(subdir=os.path.join(
            'etc/hadoop/', subdir))

    def getClusterHadoopLibNativeDir(self, subdir=''):

        return self.getClusterBinaryDir(subdir=os.path.join(
            'lib/native', subdir))
