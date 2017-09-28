#!/usr/bin/env python3

# Copyright 2017 by xiaoyang.xshaun. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Copyright (C) 2017 xiaoyang.xshaun. All Rights Reserved.

To use, simply 'pip3 install -r ./requirements/pip3-requirements.txt && python3 -B ./hbe.py'
"""

import os, yaml, logging, logging.config

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
# _logging_config is used to configue logging
# _logging_logger is used to get a logger
#
_logging_config = './config/logging.config'
_logging_logger = 'develop'

#
# _settings_file indicates where is
#
_settings_file = './settings.yaml'


#---------------------------------------------------------------------------
#   Core Logic
#---------------------------------------------------------------------------

logging.config.fileConfig(_logging_config)
logger = logging.getLogger(_logging_logger)


def _parse_settings(abspath_filename):
    try:
        if not os.path.isfile(abspath_filename):
            raise Exception('not found the setting file.')

        file = open(abspath_filename)
        ys = yaml.load(file)  # setting file with yaml format

        """
        @annotation:
            to detect necessary fields within setting file.
            to judge whether each field value is legal.
        """

        # checker
        for item in ('mode', 'codepath', 'roles', 'timelines'):
            if item not in ys:
                raise Exception(
                    "not found field '%s' in setting file." % (item))

        # checker
        if ys['mode'] not in ('pseudo_dis', 'fully_dis'):
            raise Exception("ys['mode'] has an illegal value in setting file.")

        # checker
        if ys['mode'] == 'pseudo_dis' and (
                len(ys['roles']['rm']['hosts']) != 1 or ys['roles']['rm'] != ys['roles']['nm']):
            raise Exception(
                'rm and nms must only have one, and same value under pseudo_dis mode in setting file.')

        return ys

    except Exception as e:
        logger.error(
            "catched exceptions while loading setting file: %s" % (str(e)))

    return None


def main():
    ys = _parse_settings(os.path.abspath(_settings_file))
    if ys is None:
        return 0

    try:
        for event in ys['timelines']:
            obj = __import__("timelines.%s" % (event), fromlist=True)
            func = getattr(obj, 'trigger')
            if not func(ys):
                raise Exception("errors occurs in timelines.%s" % (event))
    except Exception as e:
        logger.error(str(e))
    finally:
        return 0


if __name__ == '__main__':
    main()
