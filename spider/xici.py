#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午5:13


# 需要爬取的页面
# https://www.xicidaili.com/nn/ 高匿
# https://www.xicidaili.com/nt/ 透明

import time
from queue import Queue
from threading import Thread

import requests
from lxml import etree
from util.html import to_html
from worker.tester import Tester
from settings import DELAY, MAX_PAGE, DEBUG
from util.header import get_header


class Xici(Thread):

    def __init__(self):
        super().__init__()
        self.urls = ['https://www.xicidaili.com/nn/' + str(i + 1) + '/' for i in range(MAX_PAGE)] + \
                    ['https://www.xicidaili.com/nt/' + str(i + 1) + '/' for i in range(MAX_PAGE)]
        self.q_xici = Queue()
        self.delay = DELAY
        self.test_xici = Tester()
        self.init_queue()

    def init_queue(self):
        for url in self.urls:
            self.q_xici.put(url)

    def get_xici(self):
        if not self.q_xici.empty():
            url = self.q_xici.get()
            if DEBUG:
                print('正在爬取： ', url)
            try:
                response = requests.get(url=url, headers=get_header())
                time.sleep(self.delay)
                if response.ok:
                    resp_bytes = response.content
                    html = to_html(resp_bytes)
                    self.parse_xici(html)
            except:
                # 请求出错,将url重新放入队列
                self.q_xici.put(url)
                # 调用自身
                self.get_xici()

    def parse_xici(self, html):
        root = etree.HTML(html)
        ip_list = root.xpath("//table[@id='ip_list']//tr/td[2]/text()")
        port_list = root.xpath("//table[@id='ip_list']//tr/td[3]/text()")
        anony_list = root.xpath("//table[@id='ip_list']//tr/td[@class='country'][2]/text()")
        protocol_list = root.xpath("//table[@id='ip_list']//tr/td[6]/text()")
        data_list = [{'ip': ip_list[i], 'port': port_list[i], 'protocol': protocol_list[i].lower(),
                      'anonymity': str(anony_list[i]).replace('高匿', '1').replace('透明', '0'), } for i in
                     range(len(ip_list))]
        for data in data_list:
            self.test_xici.save_ip(data)
        self.get_xici()

    def run(self):
        self.get_xici()
