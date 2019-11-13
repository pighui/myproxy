from settings import TABLE_NAME, DATABASE_NAME, DEBUG
from web.dao import DB
import re

first_run = True


class IPDao():
    def __init__(self):
        global first_run
        self.db = DB()  # conn对象
        self.table_name = TABLE_NAME
        self.database_name = DATABASE_NAME
        self.create_table_sql = '''create table if not exists proxies(id int PRIMARY key auto_increment,
                                            ip char(20) unique not null,
                                            port char(10) not null,
                                            protocol char(10) not null,
                                            anonymity boolean,
                                            score float default 0
                                            )'''
        # 判断是否是第一次运行
        if first_run:
            # 初始化
            self.init_db()
            first_run = False

    def init_db(self):
        with self.db as c:
            c.execute('SELECT VERSION()')
            print('Database Version:', [v for v in c.fetchone().values()][0])
            # 初始化数据库
            self.data_exists()
            # 初始化数据库表
            self.table_exists()

    # 判断数据库是否存在
    def data_exists(self):
        with self.db as c:
            sql = "show databases"
            c.execute(sql)
            databases = [c.fetchall()]
            databases_list = re.findall('(\'.*?\')', str(databases))
            databases_list = [re.sub("'", '', each) for each in databases_list]
            if self.database_name in databases_list:
                print("database %s exists" % self.database_name)
            else:
                # 创建数据库
                print('database %s not exists' % self.database_name)
                sql = "create database if not exists %s default charset utf8" % self.database_name
                try:
                    c.execute(sql)
                    print("Successfully create database " + self.database_name)
                except:
                    print("Failed create database " + self.database_name)

    # 判断表是否存在
    def table_exists(self):
        with self.db as c:
            self.change_database()
            sql = "show tables"
            c.execute(sql)
            tables = c.fetchall()
            tables_list = re.findall('(\'.*?\')', str(tables))
            tables_list = [re.sub("'", '', each) for each in tables_list]
            if self.table_name in tables_list:
                print("table %s exists" % self.table_name)
            else:
                print("table %s not exists" % self.table_name)
                try:
                    c.execute(self.create_table_sql)
                    print("Successfully create table " + self.table_name)
                except:
                    print("Failed create table " + self.table_name)

    def change_database(self):
        with self.db as c:
            c.execute('use %s' % self.database_name)

    def insert(self, **item):
        sql = "insert into proxies(%s) values(%s)"
        cols = ", ".join('`{}`'.format(k) for k in item.keys())
        val_cols = ', '.join('%({})s'.format(k) for k in item.keys())
        res_sql = sql % (cols, val_cols)
        with self.db as c:
            self.change_database()
            try:
                c.execute(res_sql, args=item)
            except:
                # 插入ip重复,尝试更新
                self.update(**item)
            else:
                if DEBUG:
                    print('写入代理, %s' % ', '.join([k + ':' + str(v) for k, v in item.items()]))

    def query(self, **values):
        anonymity = values.get('anonymity')
        protocol = values.get('protocol')
        count = values.get('count')
        sql = '''select protocol, ip, port from proxies where anonymity=%s and protocol='%s' order by -score limit %s;''' % (
            anonymity, protocol, count)
        with self.db as c:
            self.change_database()
            c.execute(sql)
            result = c.fetchall()
            return result

    def query_all(self):
        with self.db as c:
            self.change_database()
            c.execute('select protocol, ip, port from proxies')
            result = c.fetchall()
        return result

    def update(self, **values):
        # 更新
        sql = 'update proxies set port=%(port)s,protocol=%(protocol)s,score=%(score)s where ip=%(ip)s'
        with self.db as c:
            self.change_database()
            try:
                c.execute(sql, args=values)
            except:
                print('更新失败')
            else:
                if DEBUG:
                    print('更新代理, ip:%s, port:%s, score:%s' % (values['ip'], values['port'], values['score']))

    def delete(self, ip):
        with self.db as c:
            self.change_database()
            try:
                c.execute('delete from proxies where ip=%s', args=(ip,))
            except:
                print('删除失败')
            else:
                if DEBUG:
                    print('删除代理, ip：' + ip)
