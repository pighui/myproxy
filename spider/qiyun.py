#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午5:31


# 需要爬取的页面
# http://www.qydaili.com/free/?action=china&page=
from queue import Queue

from lxml import etree
import time
import requests
from worker.tester import Tester
from settings import MAX_PAGE, DELAY, DEBUG
from util.header import get_header


class Qiyun():

    def __init__(self):
        self.urls = ['http://www.qydaili.com/free/?action=china&page=' + str(i + 1) + '/' for i in range(MAX_PAGE)]
        self.q_qiyun = Queue()
        self.delay = DELAY
        self.test_qiyun = Tester()
        self.init_queue()
        self.get_qiyun()

    def init_queue(self):
        for url in self.urls:
            self.q_qiyun.put(url)

    def get_qiyun(self):
        url = self.q_qiyun.get()
        if DEBUG:
            print('正在爬取： ',url)
        try:
            response = requests.get(url=url, headers=get_header())
            time.sleep(self.delay)
            if response.ok:
                html = response.text
                self.parse_qiyun(html)
        except:
            # 请求出错,将url重新放入队列
            self.q_qiyun.put(url)
            # 调用自身
            self.get_qiyun()

    def parse_qiyun(self, html):
        root = etree.HTML(html)
        ip_list = root.xpath("//table[@class='table table-bordered table-striped']/tbody/tr/td[1]/text()")
        port_list = root.xpath("//table[@class='table table-bordered table-striped']/tbody/tr/td[2]/text()")
        anony_list = root.xpath("//table[@class='table table-bordered table-striped']/tbody/tr/td[3]/text()")
        protocol_list = root.xpath("//table[@class='table table-bordered table-striped']/tbody/tr/td[4]/text()")
        data_list = [{'ip': ip_list[i], 'port': port_list[i], 'protocol': protocol_list[i].lower(),
                      'anonymity': str(anony_list[i]).replace('高匿', '1').replace('匿名', '0')} for i in
                     range(len(ip_list))]
        for data in data_list:
            self.test_qiyun.save_ip(data)
