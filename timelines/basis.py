#!/usr/bin/env python3 -B

import time, subprocess, logging, logging.config

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
#_logging_config is used to configue logging
#_logging_logger is used to get a logger
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
        self.interval = 0 # seconds

    def action(self):
        """ must be override, must return True or False """
        return True

    def finite(self):
        """ try to run several times despite failed """
        for x in range(self.attempts):
            if self.action():
                return True
            time.sleep(self.interval)
        return False

    def loop(self):
        """ try to run until succeed """
        while not self.action():
            time.sleep(self.interval)
        return True

    def once(self):
        """ try to run once despite failed """
        self.attempts = 1
        return self.finite()

    def occur(self, attempts=5, interval=5):
        """ default runtime as finite method with 5 attempts"""
        self.interval = interval
        if attempts <= 0 :
            return self.loop()
        else:
            self.attempts = attempts
            return self.finite()

class Commands(object):
    @staticmethod
    def do(arg):
        logger.info('commands.do: ' + arg)

        retcode = subprocess.call(arg, shell=True)

        logger.info('commands.do.returncode: ' + retcode)
        return retcode

    @staticmethod
    def sudo(arg, pwd):
        logger.info('commands.sudo: ' + arg)

        echo = subprocess.Popen(['echo', pwd], stdout=subprocess.PIPE, shell=False)
        sudo = subprocess.Popen(['sudo', '-S'] + arg.split(' '),
            stdin=echo.stdout, stdout=subprocess.PIPE,
            shell=False, cwd='./utility/')
        sudo.wait()

        stdout = str(sudo.stdout.read()).replace('\\n','\n')
        logger.info('commands.sudo.stdout: \n' + stdout)
        logger.info('commands.sudo.returncode: ' + str(sudo.returncode))

        return sudo.returncode

