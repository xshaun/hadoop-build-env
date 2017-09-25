#!/usr/bin/env python3 -B

import os
import yaml


class Log(object):
    """
    @TODO:
        further to support log mechnism
    """

    @staticmethod
    def info(msg):
        print('INFO: ' + msg)
        pass

    @staticmethod
    def warning(msg):
        print('WARNING: ' + msg)
        pass

    @staticmethod
    def error(msg):
        print('ERROR:' + msg)
        pass


def parse_settings(abspath_filename):
    if not os.path.isfile(abspath_filename):
        Log.error('not found the setting file.')
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
                Log.error('not found field \'' + item + '\' in setting file.')
                return None
        
        # checker
        if ys['mode'] not in ('pseudo_dis', 'fully_dis'):
            Log.error('ys[\'mode\'] has an illegal value \' in setting file.')
            return None

        # checker
        if ys['mode'] is 'pseudo_dis' and (
            len(ys['roles']['rm']) != 1 or ys['roles']['rm'] is not ys['roles']['nm']):
            Log.error('rm and nms must only have one, and same value under pseudo_dis mode in setting file.')
            return None

        return ys

    except Exception as e:
        Log.error('catched exceptions while loading setting file.')
    
    return None


def main(): 
    ys = parse_settings(os.path.abspath('./settings.yaml'))

    try:
        for event in ys['timelines']:
            obj = __import__("timelines.%s" % (event), fromlist=True)
            func = getattr(obj, event)
            if not func(ys):
                raise "errors occurs in timelines.%s" % (event)
    except Exception as e:
        Log.error(str(e))
    finally:
        return 0
    

if __name__ == '__main__':
    main()

