import os
import re
import subprocess
from loguru import logger
from appium import webdriver

from config.settings import get_all_subdirectories, load_file


def new_driver(address, capabilities):
    platformName = capabilities['platformName'].lower()
    logger.info("----创建driver实例----\n")
    driver = None
    if platformName == 'android':
        driver = webdriver.Remote(command_executor=address, desired_capabilities=capabilities)
    elif platformName == 'ios':
        driver = webdriver.Remote(command_executor=address, desired_capabilities=capabilities)
    logger.info("driver实例创建成功：%s \n" % driver)
    return driver


def _set_desired_capabilities(platformName: str, deviceName, automationName, appPackage, appActivity, **kwargs):
    capabilities = {
        "platformName": platformName,
        "deviceName": deviceName,
        "automationName": automationName,
        "appPackage": appPackage,
        "appActivity": appActivity,
    }
    if kwargs:
        for caps in kwargs:
            capabilities.update(caps)
    return capabilities


def pase_capabilities(work_path):
    # 确认capabilities.json
    capabilities_files = get_all_subdirectories(work_path, filter_name='capabilities.json')
    capabilities_absolute_path = os.path.join(work_path, capabilities_files[0])
    capabilities: dict = load_file(capabilities_absolute_path, 'json')
    if not capabilities.get('appPackage') or not isinstance(capabilities.get('appPackage'), str):
        raise

    if not capabilities.get('appActivity') or not isinstance(capabilities.get('appActivity'), str):
        raise

    return capabilities


def load_capabilities(work_path):
    # 加载配置信息
    capabilities_path = os.path.join(work_path, "capabilities.json")
    capabilities = pase_capabilities(work_path)
    return capabilities
#
# def get_devices():
#     # adb 获取Android devices设备清单
#     devices_data = os.popen("adb devices")
#
#     devices_msg = devices_data.read()
#     devices_data.close()
#
#     devices_msg = devices_msg[25:]
#
#     devices_msg_lists = devices_msg.split('\t')
#     n = 0
#     devices_lists = []
#     while n <= len(devices_msg_lists) - 1:
#         devices_lists.append(devices_msg_lists[n])
#         n += 2
#     return devices_lists


def _query_port(port):
    # 查询端口
    results = subprocess.Popen("lsof -i:%s" % (port), shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).stdout.readlines()
    return results


def _get_port(port):
    # 判断端口是否可用,不可用则自增再次查询
    results = _query_port(port)

    for item in results:
        item = item.decode()
        result_port = re.search(r"%s" % port, item)
        if result_port:
            port += 1
            _get_port(port)
    return port


def get_devices_ports(appium_port=4723, ports_num=1):
    # 获取两个可用的端口，做device实例启动的参数
    # bootstart_port会比appium_port大
    i = 0
    device_ports = []
    logger.debug("----生成可用appium server端口----\n")
    appium_port_msg = "appium server使用端口：\n"
    while i < ports_num:
        appium_port = _get_port(appium_port)
        bootstrap_port = _get_port(appium_port + 1)
        device_port = {
            "appium_port": appium_port,
            "bootstrap_port": bootstrap_port
        }
        appium_port_msg += f"appium_port:{appium_port}\n" \
                           f"bootstrap_port:{bootstrap_port}\n"
        device_ports.append(device_port)
        i += 1
    logger.debug(appium_port_msg)
    return device_ports


if __name__ == '__main__':
    print(get_devices_ports())