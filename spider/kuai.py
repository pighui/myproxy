#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午5:13


# 需要爬取的页面
# https://www.kuaidaili.com/free/inha/   高匿
# https://www.kuaidaili.com/free/intr/   透明

import time
from queue import Queue
from lxml import etree
import requests
from util.html import to_html
from worker.tester import Tester
from settings import MAX_PAGE, DELAY, DEBUG, GETTER_DELAY
from util.header import get_header


class Kuai():
    def __init__(self):
        self.urls = ['https://www.kuaidaili.com/free/inha/' + str(i + 1) + '/' for i in range(MAX_PAGE)] + \
                    ['https://www.kuaidaili.com/free/intr/' + str(i + 1) + '/' for i in range(MAX_PAGE)]
        self.q_kuai = Queue()
        self.delay = DELAY
        self.test_kuai = Tester()
        self.init_queue()
        self.get_kuai()

    def init_queue(self):
        for url in self.urls:
            self.q_kuai.put(url)

    def get_kuai(self):
        if not self.q_kuai.empty():
            url = self.q_kuai.get()
            if DEBUG:
                print('正在爬取： ', url)
            try:
                response = requests.get(url=url, headers=get_header())
                time.sleep(self.delay)
                if response.ok:
                    resp_bytes = response.content
                    html = to_html(resp_bytes)
                    self.parse_kuai(html)
            except:
                # 请求出错,将url重新放入队列
                self.q_kuai.put(url)
                # 调用自身
                self.get_kuai()

    def parse_kuai(self, html):
        root = etree.HTML(html)
        ip_list = root.xpath("//div[@id='list']//tbody/tr/td[1]/text()")
        port_list = root.xpath("//div[@id='list']//tbody/tr/td[2]/text()")
        anony_list = root.xpath("//div[@id='list']//tbody/tr/td[3]/text()")
        protocol_list = root.xpath("//div[@id='list']//tbody/tr/td[4]/text()")
        data_list = [{'ip': ip_list[i], 'port': port_list[i], 'protocol': protocol_list[i].lower(),
                      'anonymity': str(anony_list[i]).replace('高匿名', '1').replace('透明', '0')} for i in
                     range(len(ip_list))]
        for data in data_list:
            self.test_kuai.save_ip(data)
        self.get_kuai()
