#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] '
               '%(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='msohu.log'
)

class Logger(object):
    """
        日志类，用以记录程序日志
    """
    
    def error(self, message):
        logging.error(message)

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)
        
    def warning(self, message):
        logging.waring(message)
