# -*- coding: utf-8 -*-
import os
import time
from threading import current_thread

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from log import logger


def job():
    logger.info('job thread_id-{0}, process_id-{1}'.format(current_thread(), os.getpid()))
    time.sleep(3)


if __name__ == '__main__':

    executors = {
        'default': ThreadPoolExecutor(128),
        'processpool': ProcessPoolExecutor(16)
    }

    job_defaults = {
        'coalesce': False,  # 积攒的任务只跑一次
        'max_instances': 1,  # 同一任务只支持同时运行一个实例
        'misfire_grace_time': 3600  # 3600 秒的任务超时容错
    }
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone='Asia/shanghai')

    for i in range(1000):
        scheduler.add_job(job, 'interval', name='3_second_job_{}'.format(i), seconds=5)

    scheduler.start()

    while (True):
        logger.error('main 1s')
        time.sleep(1)
