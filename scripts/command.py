#!/usr/bin/env python3

from scripts.basis import logger
import subprocess
import sys

class Command(object):

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