import re
import subprocess
from threading import Thread
from time import sleep
import requests
from loguru import logger


class AppiumServer:
    """
    需要设置成单例模式
    多进程启动server
    缺少保存appium日志的方法
    """
    _port = None
    _retry = 5
    _retry_start = 2

    def start_server(self, appium_port, bootstrap_port, host, appium_log_file):
        # 启动appium
        # todo：根据devices的数量进行appium server启动
        self._port = appium_port
        cmd = "appium -a %s -p %s -bp %s" % (host, appium_port, bootstrap_port)
        with open(appium_log_file, "a") as appium_log:
            self.popen_appium = subprocess.Popen(cmd, shell=True,
                        stdout=appium_log,
                                                 stderr=subprocess.STDOUT)

        resp = self.detection_communication(appium_port, bootstrap_port, host, appium_log_file)

        if resp['status'] != 0:
            self.start_server(appium_port, bootstrap_port, host, appium_log_file)

    def kill_server(self):
        # todo：根据appium server的name 获取进程id 终止server进程
        cmd = "lsof -i:%s" % self._port
        results = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE).stdout.readlines()
        results = re.search(r"[0-9]{5}", results[1].decode())
        if results:
            results = results.group()
        kill_cmd = "kill -9 %s" %(results)
        subprocess.Popen(kill_cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def stop_server(self):
        self.popen_appium.terminate()

    def detection_communication(self, appium_port, bootstrap_port, host, appium_log_file):
        # 检测appium server是否已启动完成
        try:

            url = f"http://{host}:{appium_port}/wd/hub/status"
            resp = requests.get(url).json()
            return resp
        except Exception as error:
            # 重试次数为零
            if self._retry == 0:
                # 重新启动appium server次数为零 直接抛出错误
                if self._retry_start == 0:
                    self.kill_server()
                    logger.error("启动appium server失败：%s \n" %error)
                    raise ("启动appium server失败：%s \n" %error)
                else:
                    # 不为零 尝试重新启动appium server
                    self.stop_server()
                    self.start_server(appium_port, bootstrap_port, host, appium_log_file)
            # 重试次数不为零 则重新请求 直到请求成功 或者 重试次数为零
            self._retry -= 1
            sleep(2)
            return self.detection_communication(appium_port, bootstrap_port, host, appium_log_file)


if __name__ == '__main__':
    server = AppiumServer()
    server._port = 4723
    resp = server.detection_communication(appium_port=4723, host='127.0.0.1')
    print(resp)
    print(type(resp))