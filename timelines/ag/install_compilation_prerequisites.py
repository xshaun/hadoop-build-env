#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger


class CustomEvent(BasisEvent):

    # override
    def action(self):
        logger.info('--> timelines.ag.install_compilation_prerequisites <--')

        _shell = './utilities/t.setup_aliyun_maven_mirror.sh'
        retcode = cmd.do(_shell)
        if retcode != 0:
            return False

        _shell_in_debian = 'sudo -S ./utilities/t.install_compilation_prerequisites.sh'
        retcode = cmd.sudo(_shell_in_debian, self.ys['roles']['ag']['pwd'])
        if retcode != 0:
            return False

        # setup passphraseless
        part = dict(filter(lambda x: x[0] != 'ag', self.ys['roles'].items()))
        for k, v in part.items():
            nodes_list = ','.join([v['usr'] + '@' + n for n in v['hosts']])

            _shell = "./utilities/setup_passphraseless.sh %s %s" % (
                nodes_list, v['pwd'])
            retcode = cmd.do(_shell)
            if retcode != 0:
                return False

        return True


def trigger(ys):
    e = CustomEvent(ys, attempts=3, interval=3, auto=True)
    return e.status
