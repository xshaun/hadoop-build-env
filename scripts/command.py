#!/usr/bin/env python3

from scripts.basis import logger
from threading import Thread
import logging
import subprocess
import sys

# #
# redirect stdout, stderr to logger
#
class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass
#
#  reset stdout, stderr
#
#sys.stdout=StreamToLogger(logger, logging.INFO)
#sys.stderr=StreamToLogger(logger, logging.ERROR)
# #

class ParaIns(Thread):

    def __init__(self, ins, pwd=None):
        Thread.__init__(self)
        self.ins = ins
        self.pwd = pwd
        self.ret = True
        self.retcode = 1000

    def run(self):
        logger.info('Executing Ins : ' + self.ins)

        runins = ("source ./utilities/user.profile && %s") % (self.ins)

        try:
            echopwd = None
            process = None

            if self.pwd is None:
                process = subprocess.Popen(
                    runins, stdout=sys.stdout, stderr=sys.stdout,
                    shell=True, cwd='./', executable='/bin/bash')

            else:  # sudo
                echopwd = subprocess.Popen(
                    ['echo', self.pwd], stdout=subprocess.PIPE, shell=False)

                process = subprocess.Popen(
                    runins, stdin=echopwd.stdout, stdout=sys.stdout, stderr=sys.stdout,
                    shell=True, cwd='./', executable='/bin/bash')

            process.wait()

            self.retcode = process.returncode
            self.ret = True if self.retcode == 0 else False

        except Exception as e:
            self.retcode = -1000
            self.ret = False

        finally:
            if echopwd is not None:
                echopwd.kill()

            if process is not None:
                process.kill()

        logger.info("Ins retcode is: %d" % (self.retcode))
        logger.info('Finished Ins : ' + self.ins)

        return


class Command(object):

    @staticmethod
    def do(arg):
        logger.info('command.do: ' + arg)

        ins = ("source ./utilities/user.profile && %s") % (arg)

        process = subprocess.Popen(
            ins, stdout=sys.stdout, stderr=sys.stdout,
            shell=True, cwd='./', executable='/bin/bash')

        process.wait()

        retcode = process.returncode
        logger.info("command.do.returncode: %d" % (retcode))

        process.kill()

        return retcode

    @staticmethod
    def sudo(arg, pwd):
        logger.info('command.sudo: ' + arg)

        ins = ("source ./utilities/user.profile && %s") % (arg)

        echopwd = subprocess.Popen(
            ['echo', pwd], stdout=subprocess.PIPE, shell=False)
        process = subprocess.Popen(
            ins, stdin=echopwd.stdout, stdout=sys.stdout, stderr=sys.stdout,
            shell=True, cwd='./', executable='/bin/bash')

        process.wait()
        retcode = process.returncode

        echopwd.kill()
        process.kill()

        logger.info("command.do.returncode: %d" % (retcode))
        return retcode

    @staticmethod
    def parallel(args):
        threads = list()
        for ins in args:
            t = ParaIns(ins[0], ins[1]) if isinstance(ins, tuple) else ParaIns(ins)
            threads.append(t)
            t.start()
            t.join() # TODO, fix terminal insanity

        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = t.ret == ret
        return ret
