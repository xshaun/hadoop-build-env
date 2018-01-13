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
        self.retcode = 1000

    def run(self):
        logger.info('Executing Ins : ' + self.ins)

        # TODO redirect stdout to logger
        sys.stdout

        runins = ("source ./utilities/*.profile && %s") % (self.ins)

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
                    runins, stdin=echopwd.stdout, stdout=sys.stdout,
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

        # TODO redirect stdout to logger
        sys.stdout

        ins = ("source ./utilities/*.profile && %s") % (arg)

        process = subprocess.Popen(
            ins, stdout=sys.stdout, stderr=sys.stdout,
            shell=True, cwd='./', executable='/bin/bash')

        process.wait()
        # process_output, = process.communicate()
        # logger.info("command.do.stdout: \n %s" % (process_output))

        retcode = process.returncode
        logger.info("command.do.returncode: %d" % (retcode))

        process.kill()

        return retcode

    @staticmethod
    def sudo(arg, pwd):
        logger.info('command.sudo: ' + arg)

        # TODO redirect stdout to logger
        sys.stdout

        ins = ("source ./utilities/*.profile && %s") % (arg)

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

        echopwd.kill()
        process.kill()

        return retcode

    @staticmethod
    def parallel(args):
        threads = list()
        for ins in args:
            t = ParaIns(ins[0], ins[1]) if isinstance(ins, tuple) else ParaIns(ins)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        ret = True
        for t in threads:
            ret = t.ret == ret
        return ret
