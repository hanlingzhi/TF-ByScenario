__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: 日志类
'''

import logging
import time
import os
from colorama import Fore, Style

from util.constant import CONST
from util import global_args
from util.get_ip import get_host_ip


class LogUtil(object):

    def __init__(self, logger_name):
        # create logger
        self.logger = logging.getLogger("{}_{}".format(logger_name, global_args.get_value("uuid")))
        self.logger.setLevel(logging.DEBUG)
        # unix timestamp
        rq = time.strftime('%Y%m%d', time.localtime(time.time()))
        # set log path
        tmp_path = os.path.abspath(os.path.dirname(__file__))
        if CONST.PROJECT_E_NAME in tmp_path:
            tmp_path = "%s%s" % (tmp_path.split(CONST.PROJECT_E_NAME)[0], CONST.PROJECT_E_NAME)
        log_path = os.path.join(tmp_path, "%s/%s_%s.log" % (CONST.LOG_BASE_PATH, CONST.PROJECT_E_NAME, rq))

        # create file handler
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        # create console handler
        ch = logging.StreamHandler()
        if global_args.get_value("is_debug"):
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)

        # log format
        log_formatter = logging.Formatter(CONST.LOG_FORMAT)

        # add format handler
        fh.setFormatter(log_formatter)
        ch.setFormatter(log_formatter)

        # set logger handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self, msg):
        self.logger.debug(Fore.WHITE + str(msg) + Style.RESET_ALL)

    def info(self, msg):
        self.logger.info(Fore.GREEN + str(msg) + Style.RESET_ALL)

    def warning(self, msg):
        self.logger.warning(Fore.RED + str(msg) + Style.RESET_ALL)

    def error(self, msg):
        self.logger.error(Fore.RED + str(msg) + Style.RESET_ALL)

    def critical(self, msg):
        self.logger.critical(Fore.RED + str(msg) + Style.RESET_ALL)
