#! /usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ : pighui
# __time__ : 2019-10-31 下午4:08
import time
from multiprocessing import Process
from settings import HOST, PORT, TESTER_ENABLED, GETTER_ENABLED, API_ENABLED, DEBUG, DELAY, TESTER_DELAY, GETTER_DELAY
from web.api import ip_api
from web.app.flask_app import app
from worker.getter import Getter
from worker.tester import Tester


class Scheduler():
    def schedule_tester(self):
        print('测试器开始运行')
        tester = Tester()
        while True:
            tester.test_db_ip()
            time.sleep(TESTER_DELAY * 60)

    def schedule_getter(self):
        """
        定时获取代理
        """
        print('开始抓取代理')
        getter = Getter()
        while True:
            getter.run()
            time.sleep(1)
            print('休眠好了')
            # time.sleep(GETTER_DELAY * 60 * 60)

    def schedule_api(self):
        """
        开启API
        """
        app.register_blueprint(ip_api.blue)
        app.run(HOST, PORT, debug=DEBUG, use_reloader=False)

    def run(self):
        print('代理池开始运行')
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
            # 阻塞一会 等待web启动再运行getter和tester
            api_process.join(timeout=DELAY)
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
