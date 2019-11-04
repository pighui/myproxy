#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午5:39


import requests
from settings import TIMEOUT, TEST_URL, MAX_SCORE, VALID_STATUS_CODES, DELAY, TESTER_DELAY
from util.header import get_header
import time
from web.dao.ip_dao import IPDao


class Tester():
    def __init__(self):
        self.url = TEST_URL
        self.timeout = TIMEOUT
        self.test_dao = IPDao()

    def test_ip(self, ip_dict):

        ip = ip_dict['ip']
        protocol = ip_dict['protocol']
        port = ip_dict['port']
        try:
            start_time = time.time()
            response = requests.get(url=self.url, headers=get_header(),
                                    proxies={protocol: ip + ':' + port}, timeout=self.timeout)
            end_time = time.time()
            score = MAX_SCORE - (((end_time - start_time) / self.timeout) * MAX_SCORE)
            if score < 0:  # 偶尔会出现分数小于0的情况，原因是响应时间大于超时时间
                score = 0
            ip_dict.update({'score': round(score, 2)})
            if response.status_code in VALID_STATUS_CODES:
                return ip_dict
        except:
            return None

    # 用来测试爬取的代理是否可用
    def save_ip(self, data):
        result = self.test_ip(data)
        if result:
            # 插入代理
            self.test_dao.insert(**result)

    # 用来测试一段时间后数据库中的代理是否依然可用
    def test_db_ip(self):
        # 获取数据库中的所有代理
        try:
            all_ip = self.test_dao.query_all()
        except:
            time.sleep(DELAY)
            self.test_db_ip()
        else:
            if all_ip:
                for ip_dict in all_ip:
                    result = self.test_ip(ip_dict)
                    if result:
                        # 更新代理
                        self.test_dao.update(**result)
                    else:
                        # 删除代理
                        self.test_dao.delete(ip_dict['ip'])