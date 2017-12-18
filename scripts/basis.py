#!/usr/bin/env python3

import time
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
        # @TODO
        # support status machine
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

        return

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

        return res

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
