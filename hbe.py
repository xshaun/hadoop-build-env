#!/usr/bin/env python3

import os
import yaml
import logging
import logging.config


# # # # # # # # # # # # # # # # # # # # # 
# logging basic configure
# 
# print information 
#   -- logging.debug('logger debug message')     
#   -- logging.info('logger info message')
#   -- logging.warning('logger warning message')
#   -- logging.error('logger error message')
#   -- logging.critical('logger critical message')
#     
# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#
# create formatter
formatter = logging.Formatter(
        fmt = '[%(asctime)s %(threadName)s:%(thread)2d no:%(lineno)3d] [%(levelname)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
    )
#
# create console handler and set level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
#
# # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # 
# Create a filehandler and add to logger
if not os.path.exists('log/'): 
    os.makedirs('log/');
fh = logging.FileHandler('./log/hbe.log')  
fh.setFormatter(formatter)  
logger.addHandler(fh)
#
# # # # # # # # # # # # # # # # # # # # # 


def parse_settings(abspath_filename):
    if not os.path.isfile(abspath_filename):
        logging.error('not found the setting file.')
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
                logging.error('not found field \'' + item + '\' in setting file.')
                return None
        
        # checker
        if ys['mode'] not in ('pseudo_dis', 'fully_dis'):
            logging.error('ys[\'mode\'] has an illegal value \' in setting file.')
            return None

        # checker
        if ys['mode'] is 'pseudo_dis' and (
            len(ys['roles']['rm']) != 1 or ys['roles']['rm'] is not ys['roles']['nm']):
            logging.error('rm and nms must only have one, and same value under pseudo_dis mode in setting file.')
            return None

        return ys

    except Exception as e:
        logging.error('catched exceptions while loading setting file.')
    
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
        logging.error(str(e))
    finally:
        return 0
    

if __name__ == '__main__':
    main()

