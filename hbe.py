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

To use, simply 'python3 -B ./hbe.py'
"""

import os, yaml, logging, logging.config

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
#_logging_config is used to configue logging
#_logging_logger is used to get a logger
#
_logging_config = './config/logging.config'
_logging_logger = 'develop'

#
#_settings_file indicates where is 
#
_settings_file = './settings.yaml'


#---------------------------------------------------------------------------
#   Core Logic
#---------------------------------------------------------------------------

logging.config.fileConfig(_logging_config)
logger = logging.getLogger(_logging_logger)

def _parse_settings(abspath_filename):
    if not os.path.isfile(abspath_filename):
        logger.error('not found the setting file.')
        return None

    try:
        file = open(abspath_filename)
        ys = yaml.load(file) # setting file with yaml format

        """
        @annotation:
            to detect necessary fields within setting file.
            to judge whether each field value is legal.
        """
        
        # checker
        for item in ('mode', 'codepath', 'roles', 'timelines'):
            if item not in ys:
                logger.error('not found field \'' + item + '\' in setting file.')
                return None
        
        # checker
        if ys['mode'] not in ('pseudo_dis', 'fully_dis'):
            logger.error('ys[\'mode\'] has an illegal value \' in setting file.')
            return None

        # checker
        if ys['mode'] is 'pseudo_dis' and (
            len(ys['roles']['rm']) != 1 or ys['roles']['rm'] is not ys['roles']['nm']):
            logger.error('rm and nms must only have one, and same value under pseudo_dis mode in setting file.')
            return None

        return ys

    except Exception as e:
        logger.error('catched exceptions while loading setting file.')
    
    return None


def main(): 
    ys = _parse_settings(os.path.abspath(_settings_file))

    try:
        for event in ys['timelines']:
            obj = __import__("timelines.%s" % (event), fromlist=True)
            func = getattr(obj, event.split('.')[-1]) # function name
            if not func(ys):
                raise Exception("errors occurs in timelines.%s" % (event))
    except Exception as e:
        logger.error(str(e))
    finally:
        return 0
    

if __name__ == '__main__':
    main()

