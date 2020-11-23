"""
启动文件
1.设备信息
2.appium server信息
3.进程数量
4.pytest.main配置
"""
import json
import os
from datetime import datetime
import pytest

import config
from base.BaseAdb import AndroidDebugBridge
from base.BasePhoneInfo import PhoneInfo
from base.make import initialize_dir
from base.mobile_core import get_devices_ports
from base.BaseAppiumServer import AppiumServer
from multiprocessing import Pool, Process
from loguru import logger
from base.file_plugin import mkdir_dir, load_file


def get_device_info(device_id):
    device_info = {}
    device_info['device_id'] = device_id
    phoneinfo = PhoneInfo('android', device_id).get_device_info()
    device_info.update(phoneinfo)
    return device_info


def cli():
    pass


def main():
    """
    初始化UI自动化操作：
    1.初始化log日志文件夹
        1.appium log
        2.自动化日志
    2.初始化图片文件夹
        1.失败截图
        2.运行截图
    需要获取运行的绝对路径
    :return:
    """
    # 从命令行读取 或者通过获取运行路径
    test_path = '/Users/yewenkai/PycharmProjects/us_appium/examples'
    # 获取当前时间
    specific_time = datetime.now().strftime("%Y%m%d%H%M%S")

    ini_dirs = initialize_dir(test_path)

    # 初始化logger日志文件
    log_file = os.path.join(ini_dirs["work_tests_log"], f"{specific_time}.run.main.log")
    logger.add(log_file)

    # 生成allure2日志报告存放路径
    allure2_report_path = mkdir_dir(test_path, "allure_report")

    log_msg = f"log日志路径：{ini_dirs['work_log_path']}\n"
    log_msg += f"图片文件路径：{ini_dirs['work_img_path']}\n"
    log_msg += f"allure2日志报告路径：{allure2_report_path}\n"
    # 记录log、图片日志
    logger.debug(log_msg)

    # 获取devices_id
    baseadb = AndroidDebugBridge()
    devices = baseadb.get_devices()

    # 记录设备id
    logger.info(json.dumps(device) + "\n" for device in devices)

    # 加载基础配置信息

    #################### 新版本修改
    settings_file = os.path.join(test_path, "settings.ini")
    settings_ini = load_file(settings_file, load_type="ini")

    driver_caps_list = settings_ini.items("driver_caps")

    appium_server_port = int(settings_ini.get("appium_caps", "appium_port"))
    host = settings_ini.get("appium_caps", "host")

    driver_caps = {}
    for driver_cap in driver_caps_list:
        driver_caps[driver_cap[0]] = driver_cap[1]

    # 根据命令行传入参数来确定并发进程的数量，根据获取的devices_id来确认实际启动的进程数量
    # auto=用例数量？ or 设备数量？ or CPU核数？
    # 进程数
    proc_num = 2
    # 获取实际启动进程的数量，需要进行判断。以proc_num为主
    start_num = proc_num if proc_num < len(devices) else len(devices)
    logger.info("启动进程数量为：%s \n" % start_num)

    # 获取ports
    appium_ports = get_devices_ports(appium_port=appium_server_port, ports_num=start_num)

    # 根据启动进程数量来加载设备数,顺序加载

    devices_info = {}
    for i in range(start_num):
        device_info = get_device_info(devices[i])
        devices_info[device_info["device_name"]] = {
            "using_state": "no",
            "host": host,
            "appium_server_ports": {
                "appium_port": appium_ports[i]["appium_port"],
                "bootstrap_port": appium_ports[i]["bootstrap_port"],
            },
            "caps": {
                "platformVersion": device_info["platformVersion"],
                "deviceName": devices[i],
            }
        }
        devices_info[device_info["device_name"]]["caps"].update(driver_caps)
    # 写入临时文件
    temporary_caps_file = os.path.join(test_path, "capabilities.json")
    with open(temporary_caps_file, "w") as caps_file:
        json.dump(devices_info, caps_file)
    # +"/test_main.py::TestMain::test_article_action"
    cmd = ["-v", test_path]
    if start_num > 1:
        cmd.append(f"-n={start_num}")

    cmd.append(f"--alluredir={allure2_report_path}")
    config.driver = None
    pytest.main(cmd)
    # allure生成报告的路径
    allure_html_file = os.path.join(test_path, "allure_html_report")
    os.system(f"allure generate {allure2_report_path} -o {allure_html_file} --clean")


if __name__ == '__main__':
    main()
    print("运行结束")
