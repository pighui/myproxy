#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午5:33


# 需要爬取的页面
# http://www.66ip.cn/index.html
from queue import Queue

from lxml import etree
import time
import requests
from worker.tester import Tester
from settings import MAX_PAGE, DELAY, DEBUG
from util.header import get_header
from util.html import to_html


class Ssfree():

    def __init__(self):
        self.urls = ['http://www.66ip.cn/%s.html' % str(i + 1) for i in range(MAX_PAGE)]
        self.q_ssfree = Queue()
        self.delay = DELAY
        self.test_ssfree = Tester()
        self.init_queue()
        self.get_ssfree()

    def init_queue(self):
        for url in self.urls:
            self.q_ssfree.put(url)

    def get_ssfree(self):
        url = self.q_ssfree.get()
        if DEBUG:
            print('正在爬取： ',url)
        try:
            response = requests.get(url=url, headers=get_header())
            time.sleep(self.delay)
            if response.ok:
                resp_bytes = response.content
                html = to_html(resp_bytes)
                self.parse_ssfree(html)
        except:
            # 请求出错,将url重新放入队列
            self.q_ssfree.put(url)
            # 调用自身
            self.get_ssfree()

    def parse_ssfree(self, html):
        root = etree.HTML(html)
        ip_list = root.xpath("//div[@align='center']//table//tr/td[1]/text()")[1:]
        port_list = root.xpath("//div[@align='center']//table//tr/td[2]/text()")[1:]
        anony_list = root.xpath("//div[@align='center']//table//tr/td[4]/text()")[1:]
        protocol_list = ''
        if ip_list:
            data_list = [{'ip': ip_list[i], 'port': port_list[i], 'protocol': 'http',
                          'anonymity': anony_list[i].replace('高匿代理', '1').replace('匿名代理', '1')} for i in
                         range(len(ip_list))]
            for data in data_list:
                self.test_ssfree.save_ip(data)
