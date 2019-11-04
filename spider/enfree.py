#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午5:31


# 需要爬取的页面
# http://www.89ip.cn/index.html
from queue import Queue

from lxml import etree
import time
import requests

from util.html import to_html
from worker.tester import Tester
from settings import MAX_PAGE, DELAY, DEBUG
from util.header import get_header


class Enfree():

    def __init__(self):
        self.urls = ['http://www.89ip.cn/index_%s.html' % str(i + 1) for i in range(MAX_PAGE)]
        self.q_enfree = Queue()
        self.delay = DELAY
        self.test_enfree = Tester()
        # 初始化队列
        self.init_queue()
        # 运行爬虫
        self.get_enfree()

    def init_queue(self):
        for url in self.urls:
            self.q_enfree.put(url)

    def get_enfree(self):
        url = self.q_enfree.get()
        if DEBUG:
            print('正在爬取： ',url)
        try:
            response = requests.get(url=url, headers=get_header())
            time.sleep(self.delay)
            if response.ok:
                resp_bytes = response.content
                html = to_html(resp_bytes)
                self.parse_enfree(html)
        except:
            # 请求出错,将url重新放入队列
            self.q_enfree.put(url)
            # 调用自身
            self.get_enfree()

    def parse_enfree(self, html):
        root = etree.HTML(html)
        ip_list = root.xpath("//table[@class='layui-table']/tbody/tr/td[1]/text()")
        port_list = root.xpath("//table[@class='layui-table']/tbody/tr/td[2]/text()")
        anony_list = ''
        protocol_list = ''
        data_list = [{'ip': ip_list[i].replace('\n', '').replace('\t', ''),
                      'port': port_list[i].replace('\n', '').replace('\t', ''), 'protocol': 'http',
                      'anonymity': '0'} for i in
                     range(len(ip_list))]
        for data in data_list:
            self.test_enfree.save_ip(data)
