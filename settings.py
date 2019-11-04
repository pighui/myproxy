#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-30 下午6:52

# 爬取页数
MAX_PAGE = 10

# 请求间隔时间(s)
DELAY = 2

# 测试代理超时时间(s)
TIMEOUT = 20

# 代理分数
MAX_SCORE = 100

# 响应码
VALID_STATUS_CODES = [200, 302]

# 测试用的目标地址
TEST_URL = 'http://httpbin.org/get'

# 自动测试数据库中的ip的时间间隔(min)
TESTER_DELAY = 30

# 自动获取代理的间隔时间(h)
GETTER_DELAY = 2

# mysql数据库配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'xuhui19951203',
    'charset': 'utf8'
}

# 数据库名
DATABASE_NAME = 'proxy'
# 数据库表名
TABLE_NAME = 'proxies'

# flask配置
HOST = '0.0.0.0'
# 设置端口
PORT = '8880'

# 是否启动测试器
TESTER_ENABLED = True

# 是否启动爬取器
GETTER_ENABLED = True

# 是否启动web接口
API_ENABLED = True

# 是否开启调试模式
DEBUG = True
