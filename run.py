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
from base.BaseAdb import AndroidDebugBridge
from base.BasePhoneInfo import PhoneInfo
from base.mobile_core import get_devices_ports, load_capabilities
from base.BaseAppiumServer import AppiumServer
from multiprocessing import Pool, Process
from loguru import logger
from config.settings import mkdir_file


def get_device_info(device_id):
    device_info = {}
    device_info['device_id'] = device_id
    phoneinfo = PhoneInfo('android', device_id).get_device_info()
    device_info.update(phoneinfo)
    return device_info

#
# def appium_server(appium_port, bootstrap_port, host='127.0.0.1'):
#     # appium_server = RunServer(AppiumServer, appium_port=appium_port, bootstrap_port=bootstrap_port, host=host)
#     # return appium_server
#     .start_server(appium_port=appium_port, bootstrap_port=bootstrap_port, host=host)

def process_main(test_path, work_log_file, work_img_file, appium_ports, device_id, capabilitie, external_cmd: list):
    # 多进程启动入口
    # todo:需要读取配置文件获取 appium_port、host

    # 创建一个appium log日志文件
    # 创建一个自动化日志文件
    # 需要区分多进程的日志
    # 每个日志开头记录设备信息 进程信息 时间日期 运行用例文件路径
    process_pid = str(os.getpid())
    appium_log_file = os.path.join(work_log_file, f"{process_pid}_appium.log")

    tests_log_name = "driver_id+drvier_name.log"

    # 启动appium server
    logger.info("----启动appium server----\n")
    host = capabilitie.pop("host")
    appium_host = host.split('//')[1]

    logger.debug("appium host:%s \n" % appium_host)

    appium_server = AppiumServer()
    appium_server.start_server(appium_ports['appium_port'], appium_ports['bootstrap_port'], appium_host, appium_log_file)

    # 获取设备信息
    device_info = get_device_info(device_id)

    # 设置driver 配置
    devices_capabilitie = {
        "platformName": "Android",
        "platformVersion": device_info['platformVersion'],
        "deviceName": device_info['device_id'],
        "automationName": "uiautomator2",
    }
    # 设置driver启动地址
    driver_address = "%s:%s/wd/hub" % (host, appium_ports['appium_port'])
    devices_capabilitie['driver_address'] = driver_address
    # 添加用户配置的driver配置参数
    devices_capabilitie.update(capabilitie)

    # 记录设备信息
    device_info_msg = json.dumps(device_info)
    logger.info(device_info_msg + "\n")

    # 记录driver配置信息
    devices_capabilitie_msg = json.dumps(devices_capabilitie)
    logger.info(devices_capabilitie_msg + "\n")

    # 启动pytest
    logger.info("----启动pytest.main---- \n")
    logger.info("测试路径为: %s \n" % test_path)

    cmd = [test_path, f'--cmdopt={devices_capabilitie}']
    cmd.extend(external_cmd)
    logger.info("pytest 命令行内容：%s \n" % json.dumps(cmd))

    pytest.main(cmd)
    appium_server.stop_server()


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
    test_path = '/Users/yewenkai/PycharmProjects/us_appium/tests'

    cunrrent_time = datetime.now().strftime("%Y%m%d")
    specific_time = datetime.now().strftime("%Y%m%d%H%M%S")

    work_log_path = test_path + "/log/"
    work_img_path = test_path + "/img/"

    if not os.path.isdir(work_log_path):
        # 创建一个log日志文件夹
        work_log_path = mkdir_file(test_path, "log")

    if not os.path.isdir(work_img_path):
        work_img_path = mkdir_file(test_path, "img")

    # 创建一个log日志文件夹
    work_log_file = mkdir_file(work_log_path, cunrrent_time)
    # 创建一个图片文件夹
    work_img_file = mkdir_file(work_img_path, cunrrent_time)

    # 初始化logger日志文件
    log_file = os.path.join(work_log_file, f"{specific_time}.run.log")
    logger.add(log_file)

    # 生成allure2日志报告存放路径
    allure2_report_path = mkdir_file(test_path, "allure_report")

    log_msg = f"log日志路径：{work_log_file}\n"
    log_msg += f"图片文件路径：{work_img_file}\n"
    log_msg += f"allure2日志报告路径：{allure2_report_path}\n"
    # 记录log、图片日志
    logger.debug(log_msg)

    # 获取devices_id
    baseadb = AndroidDebugBridge()
    devices = baseadb.get_devices()

    # 记录设备id
    logger.info(json.dumps(device) + "\n" for device in devices)

    # 加载基础配置信息
    devices_capabilitie = load_capabilities(test_path)
    # 获取appium server想要起始的端口号
    appium_server_port = devices_capabilitie.pop("appium_server_port")

    # 根据命令行传入参数来确定并发进程的数量，根据获取的devices_id来确认实际启动的进程数量
    # auto=用例数量？ or 设备数量？ or CPU核数？
    # 进程数
    proc_num = 2
    # 获取实际启动进程的数量，需要进行判断。以proc_num为主
    start_num = proc_num if proc_num < len(devices) else len(devices)

    # 获取prots
    appium_ports = get_devices_ports(appium_port=appium_server_port, ports_num=start_num)

    external_cmd = []
    # external_cmd.extend([f"--alluredir={allure2_report_path}"])

    # 启动进程，创建进程池
    # pool = Pool()
    process_list = []
    for i in range(start_num):
        # devices_capabilitie = {
        #     "appPackage": "com.xueqiu.android",
        #     "appActivity": ".view.WelcomeActivityAlias",
        #     "app": "/Users/yewenkai/PycharmProjects/us_appium/apk/com.xueqiu.android_12.18.1_280.apk"
        # }
        proces = Process(target=process_main, args=(test_path, work_log_file, work_img_file,
                                                    appium_ports[i], devices[i],
                                                    devices_capabilitie, external_cmd))
        process_list.append(proces)

    for proces in process_list:
        proces.start()

        proces_log_msg = "----启动进程----\n"
        proces_log_msg += "----启动进程id：%s \n" %proces.pid
        logger.info(proces_log_msg)

        print("进程id：%s" % proces.pid)
    for proces in process_list:
        proces.join()

        logger.info("----进程结束:%s \n" % proces.pid)

        print("等待子进程结束")

    # for proces in process_list:
    #     proces.close()
    #     pool.apply_async(main, devices_capabilitie)
    # pool.close()
    # pool.join()


if __name__ == '__main__':
    main()
    print("运行结束")
