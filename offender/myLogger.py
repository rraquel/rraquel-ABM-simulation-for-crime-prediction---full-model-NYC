#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging,os,time

dir_path = os.path.dirname(os.path.realpath(__file__))

# set up logging to file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=os.path.join(dir_path,'..','output','offender.{}.log'.format(time.strftime('%Y%m%d_%H%M%S'))),
                    filemode='w+')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)