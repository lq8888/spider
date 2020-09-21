#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import os.path
import time


def get_logger():

    # 第一步，创建一个logger
    logger = logging.getLogger('Spider_Logger')
    logger.setLevel(logging.INFO)
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.path.dirname(os.path.dirname(os.getcwd())) + '/logs/'
    log_name = log_path + rq + '.logs'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)

    return logger
