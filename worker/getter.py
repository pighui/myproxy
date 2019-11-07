#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-31 下午8:02


from threading import Thread
from spider.enfree import Enfree
from spider.kuai import Kuai
from spider.qiyun import Qiyun
from spider.ssfree import Ssfree
from spider.xici import Xici


class Getter(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        ssfree_spider = Ssfree()
        enfree_spider = Enfree()
        kuai_spider = Kuai()
        qiyun_spider = Qiyun()
        xici_spider = Xici()
        thread_list = [ssfree_spider, enfree_spider, kuai_spider, qiyun_spider, xici_spider]
        # 启动线程
        for t in thread_list:
            t.start()
