#!/usr/bin/env python3

from scripts.basis import logger
from threading import Thread
import subprocess
import sys


class ParaIns(Thread):

    def __init__(self, ins, pwd=None):
        Thread.__init__(self)
        self.ins = ins
        self.pwd = pwd
        self.ret = True
        self.retcode = 0

    def run(self):
        logger.info('Executing Ins : ' + self.ins)

        # @TODO
        # redirect stdout to logger
        sys.stdout

        runins = "source ./utilities/*.profile && %s " % (self.ins)

        process = None

        if self.pwd is None: 
            process = subprocess.Popen(
                runins, stdout=sys.stdout, stderr=sys.stdout,
                shell=True, cwd='./', executable='/bin/bash')

        else: # sudo
            echopwd = subprocess.Popen(
                ['echo', self.pwd], stdout=subprocess.PIPE, shell=False)

            process = subprocess.Popen(
                runins, stdin=echopwd.stdout, stdout=sys.stdout,
                shell=True, cwd='./', executable='/bin/bash')

        process.wait()

        self.retcode = process.returncode
        self.result = True if self.retcode == 0 else False

        logger.info("Ins retcode is: %d" % (self.retcode))
        logger.info('Finished Ins : ' + this.ins)

        return


class Command(Object):

    @staticmethod
    def do(arg):
        logger.info('command.do: ' + arg)

        # @TODO
        # redirect stdout to logger
        sys.stdout

        ins = "source ./utilities/*.profile && %s" % (arg)
        process = subprocess.Popen(
            ins, stdout=sys.stdout, stderr=sys.stdout,
            shell=True, cwd='./', executable='/bin/bash')

        process.wait()
        # process_output, = process.communicate()
        # logger.info("command.do.stdout: \n %s" % (process_output))

        retcode = process.returncode
        logger.info("command.do.returncode: %d" % (retcode))

        return retcode

    @staticmethod
    def sudo(arg, pwd):
        logger.info('command.sudo: ' + arg)

        # @TODO
        # redirect stdout to logger
        sys.stdout

        ins = "source ./utilities/*.profile && %s " % (arg)
        echopwd = subprocess.Popen(
            ['echo', pwd], stdout=subprocess.PIPE, shell=False)
        process = subprocess.Popen(
            ins, stdin=echopwd.stdout, stdout=sys.stdout,
            shell=True, cwd='./', executable='/bin/bash')

        process.wait()
        # process_output, = process.communicate()
        # logger.info("command.do.stdout: \n %s" % (process_output))

        retcode = process.returncode
        logger.info("command.do.returncode: %d" % (retcode))

        return retcode
