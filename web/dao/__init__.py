"""
Database Access Object
"""
import pymysql
from pymysql.cursors import DictCursor
from settings import DB_CONFIG

class DB():
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        # print('--Connect database OK--')

    def __enter__(self):
        # 检查当前连接是否有效
        self.conn.ping(reconnect=True)
        # 进入上下文时，需要返回一个cursor对象
        return self.conn.cursor(cursor=DictCursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 判断是否正常的方式退出上下文
        if not exc_type:
            # 如果是正常情况，则提交事务
            self.conn.commit()
        else:
            # 如果非正常，则回滚事务
            self.conn.rollback()

    def close(self):
        self.conn.close()