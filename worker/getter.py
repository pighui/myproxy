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


class Getter():
    def __init__(self):
        self.ssfree_spider = Ssfree()
        self.enfree_spider = Enfree()
        self.kuai_spider = Kuai()
        self.qiyun_spider = Qiyun()
        self.xici_spider = Xici()
        self.task_list = [self.ssfree_spider, self.enfree_spider, self.kuai_spider, self.qiyun_spider, self.xici_spider]
        self.thread_list = []
        # 创建线程列表
        for task in self.task_list:
            t = threading.Thread(target=task)
            self.thread_list.append(t)

    def run(self):
        # 启动线程
        for thread in self.thread_list:
            thread.setDaemon(True)
            thread.start()
        for thread in self.thread_list:
            thread.join()
