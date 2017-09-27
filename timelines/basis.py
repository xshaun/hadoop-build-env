#!/usr/bin/env python3 -B

import sys
import time
import subprocess
import logging
import logging.config

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
# _logging_config is used to configue logging
# _logging_logger is used to get a logger
#
_logging_config = './config/logging.config'
_logging_logger = 'develop'

#---------------------------------------------------------------------------
#   Core Logic
#---------------------------------------------------------------------------

logging.config.fileConfig(_logging_config)
logger = logging.getLogger(_logging_logger)


class BasisEvent(object):
    """
    @attributes:
     ys:  settting yaml file
     attempts:  times trying to do
     interval:  pause time while failed to run
    """

    def __init__(self, ys):
        self.ys = ys
        self.attempts = 0
        self.interval = 0  # seconds

    def action(self):
        """ must be override, must return True or False """
        return True

    def finite(self):
        """ try to run several times despite failed """
        for x_x in range(self.attempts):
            if self.action():
                return True
            logger.info("!'o'! a failed attempt at %d-th running" % (x_x))
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

    def occur(self, attempts=5, interval=5):
        """ default runtime as finite method with 5 attempts"""
        self.interval = interval
        if attempts <= 0:
            return self.loop()
        else:
            self.attempts = attempts
            return self.finite()


class Commands(object):

    @staticmethod
    def do(arg):
        logger.info('commands.do: ' + arg)

        # @TODO
        # redirect stdout to logger
        sys.stdout

        process = subprocess.Popen(arg,
                                   stdout=sys.stdout, stderr=sys.stdout,
                                   shell=True, cwd='./')

        process.wait()
        # process_output, = process.communicate()
        # logger.info("commands.do.stdout: \n %s" % (process_output))

        retcode = process.returncode
        logger.info("commands.do.returncode: %d" % (retcode))
        return retcode

    @staticmethod
    def sudo(arg, pwd):
        logger.info('commands.sudo: ' + arg)

        # @TODO
        # redirect stdout to logger
        sys.stdout

        echopwd = subprocess.Popen(['echo', pwd],
                                   stdout=subprocess.PIPE, shell=True)
        process = subprocess.Popen(arg,
                                   stdin=echopwd.stdout, stdout=sys.stdout, stderr=sys.stdout,
                                   shell=True, cwd='./')

        echopwd.stdout.close()
        process.wait()
        # process_output, = process.communicate()
        # logger.info("commands.do.stdout: \n %s" % (process_output))

        retcode = process.returncode
        logger.info("commands.do.returncode: %d" % (retcode))
        return retcode
