#!/usr/bin/env python3 -B

import time, subprocess

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
        return subprocess.call(arg, shell=True)

    @staticmethod
    def sudo(arg, pwd):
        echo = subprocess.Popen(['echo', pwd], stdout=subprocess.PIPE, shell=False)
        #print('echo:' + str(echo.stdout.read()))
        sudo = subprocess.Popen(['sudo','-S', '/bin/sh', '-c', arg],
            stdin=echo.stdout, stdout=subprocess.PIPE,
            shell=False, cwd='./utility/')
        sudo.wait()
        #print('returncode:' + str(sudo.returncode))
        print('sudo.stdout:')

        map(print, [i for i in str(sudo.stdout.read()).split('\\n')])
        print(sudo.returncode)
        return sudo.returncode

