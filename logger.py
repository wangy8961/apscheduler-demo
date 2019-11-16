#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : logger.py
# @Author : Madman
# @Date   : 2019/11/16 15:21
import logging
import os
import time

import coloredlogs


#-----------------------------------------------------------------------------
# 创建或获取 Logger 实例
#-----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# APScheduler 模块使用的日志实例
aps_logger1 = logging.getLogger('apscheduler.scheduler')
aps_logger2 = logging.getLogger('apscheduler.executors.default')


#-----------------------------------------------------------------------------
# 设置日志格式
#-----------------------------------------------------------------------------

fmt = '%(asctime)s - [%(name)s] - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
formatter = logging.Formatter(fmt)


#-----------------------------------------------------------------------------
# 创建 Handler, 输出日志到控制台和文件
#-----------------------------------------------------------------------------

# 日志文件 FileHandler
basedir = os.path.abspath(os.path.dirname(__file__))
log_dest = os.path.join(basedir, 'logs')  # 日志文件所在目录
if not os.path.isdir(log_dest):
    os.mkdir(log_dest)
filename = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + '.log'  # 日志文件名，以当前时间命名
file_handler = logging.FileHandler(os.path.join(log_dest, filename), encoding='utf-8')  # 创建日志文件handler
file_handler.setFormatter(formatter)  # 设置Formatter

# 控制台日志 StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


#-----------------------------------------------------------------------------
# 为 Logger 添加 Handler
#-----------------------------------------------------------------------------

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
aps_logger1.addHandler(file_handler)
aps_logger1.addHandler(stream_handler)
aps_logger2.addHandler(file_handler)
aps_logger2.addHandler(stream_handler)


#-----------------------------------------------------------------------------
# 设置日志级别
#-----------------------------------------------------------------------------

logger.setLevel(logging.DEBUG)
aps_logger1.setLevel(logging.DEBUG)
aps_logger2.setLevel(logging.DEBUG)


#-----------------------------------------------------------------------------
# 当日志输出到控制台时，会带有颜色
#-----------------------------------------------------------------------------

coloredlogs.DEFAULT_FIELD_STYLES = dict(
    asctime=dict(color='green'),
    name=dict(color='blue'),
    filename=dict(color='magenta'),
    lineno=dict(color='cyan'),
    levelname=dict(color='black', bold=True),
)
coloredlogs.install(fmt=fmt, level='DEBUG', logger=logger)
coloredlogs.install(fmt=fmt, level='DEBUG', logger=aps_logger1)
coloredlogs.install(fmt=fmt, level='DEBUG', logger=aps_logger2)
