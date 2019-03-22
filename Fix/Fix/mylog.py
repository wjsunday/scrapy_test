#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import getpass
import time


class MyLog(object):
    def __init__(self):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)
        self.logFile = "./log/"+str(time.strftime("%Y%m%d_%H%M")) + '.log'
        self.formatter = logging.Formatter('%(asctime)-15s  |  %(message)-12s',"%Y-%m-%d %H:%M:%S")

        self.logHand = logging.FileHandler(self.logFile, encoding='utf8')
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.DEBUG)

        self.logger.addHandler(self.logHand)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)


if __name__ == '__main__':
    mylog = MyLog()

