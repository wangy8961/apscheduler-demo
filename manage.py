# -*- coding: utf-8 -*-
import os
import time
from threading import current_thread

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from logger import logger


def job():
    """耗时 30 秒的函数"""
    logger.info('job thread_id-{0}, process_id-{1}'.format(current_thread(), os.getpid()))
    time.sleep(30)


if __name__ == '__main__':

    executors = {
        'default': ThreadPoolExecutor(128),
        'processpool': ProcessPoolExecutor(16)
    }

    job_defaults = {
        'coalesce': True,  # 错过执行时间后的同一任务，原本需要被排队执行多次，但现在只执行一次
        'max_instances': 1,  # 同一任务只支持同时运行一个实例
        'misfire_grace_time': 3600  # 3600 秒的任务超时容错
    }
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone='Asia/shanghai')

    for i in range(1000):
        # 调度 1000 个任务，每个任务都是间隔 5 秒执行一次 job 函数（耗时 30 秒）
        scheduler.add_job(job, 'interval', name='3_second_job_{}'.format(i), seconds=5)

    scheduler.start()

    while (True):
        logger.error('main 1s')
        time.sleep(1)
