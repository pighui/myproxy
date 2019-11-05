#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-11-2 上午11:51


import requests


def get_proxies(params: dict = {}):
    '''
    :param params: 参数字典 默认为空
    :return: 返回一个包含多条代理信息的列表，列表的每一个元素是一个字典
    '''
    try:
        response = requests.get('http://127.0.0.1:8888/ip/', params=params)
        if response.status_code == 200:
            result = response.json()
            return [{d['protocol']: 'http://' + d['ip'] + ':' + d['port']} for d in result]
    except ConnectionError:
        return None


def random_proxy():
    '''
    :return: 返回一个代理信息字典
    '''
    try:
        response = requests.get('http://127.0.0.1:8888/ip/random/')
        if response.status_code == 200:
            result = response.json()
            return result
    except ConnectionError:
        return None


if __name__ == '__main__':
    # 获取一条代理
    ip1 = get_proxies()
    print(ip1)
    # 获取多条代理
    ip2 = get_proxies({'count': 3})
    print(ip2)
    # 获取匿名代理
    ip3 = get_proxies({'anonymity': 1})
    print(ip3)
    # 获取https代理
    ip4 = get_proxies({'protocol': 'https'})
    print(ip4)
    # 获取多条匿名的https代理
    ip5 = get_proxies({'count': 3, 'anonymity': 1, 'protocol': 'https'})
    print(ip5)
    # 随机获取一条代理
    ip6 = random_proxy()
    print(ip6)
