#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-31 下午8:02
import threading
from spider.enfree import Enfree
from spider.kuai import Kuai
from spider.qiyun import Qiyun
from spider.ssfree import Ssfree
from spider.xici import Xici


class Getter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        ssfree_spider = Ssfree()
        enfree_spider = Enfree()
        kuai_spider = Kuai()
        qiyun_spider = Qiyun()
        xici_spider = Xici()
        task_list = [ssfree_spider, enfree_spider, kuai_spider, qiyun_spider, xici_spider]
        thread_list = []

        # 创建线程列表
        for task in task_list:
            t = threading.Thread(target=task)
            thread_list.append(t)

        # 启动线程
        for thread in thread_list:
            thread.setDaemon(True)
            thread.start()
        for thread in thread_list:
            thread.join()
