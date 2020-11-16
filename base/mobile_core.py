import os, json
import re
import subprocess
from loguru import logger
from appium import webdriver

from base.file_plugin import get_all_subdirectories, load_file


def new_driver(address, appium_port, driver_capabilities):
    """
    1.加载配置文件
    2.开启appium server
    3.创建driver实例
    :param address:
    :param capabilities:
    :return:
    """
    # 启动appium server
    ## 获取appium port、bootstrap port

    # 获取driver Remote地址、driver配置信息
    # driver_capabilities = data['driver_caps']

    driver_address = f"http://{address}:{appium_port}/wd/hub"
    driver_caps_log_msg = f"driver address：{driver_address} \n"
    driver_caps_log_msg += f"driver caps：{json.dumps(driver_capabilities)} \n"
    logger.debug(driver_caps_log_msg)
    # todo:记录device配置信息

    # 创建driver实例
    platformName = driver_capabilities['platformName'].lower()
    logger.info("----创建driver实例----\n")
    driver = None
    if platformName == 'android':
        driver = webdriver.Remote(command_executor=driver_address, desired_capabilities=driver_capabilities)
    elif platformName == 'ios':
        driver = webdriver.Remote(command_executor=driver_address, desired_capabilities=driver_capabilities)

    logger.info("driver实例创建成功：%s \n" % driver)
    return driver


def pase_capabilities(work_path):
    # 确认capabilities.json
    """
    配置信息格式：
    data = {
        "global_env": {
            "host": "127.0.0.1",
            "appium_server_port": 4723
        }
        "caps": {}
    }
    返回信息：
    data = {
        "global_env": {
            "host": "127.0.0.1",
            "appium_server_port": 4723
        }
        "driver_caps": {}, driver 实例配置信息
        "device_caps": {}, device 设备配置信息
    }
    :param work_path:
    :return:
    """
    # 获取工作目录下的caps.json文件绝对路径
    capabilities_files = get_all_subdirectories(work_path, filter_name='capabilities.json')
    capabilities_absolute_path = os.path.join(work_path, capabilities_files[0])
    # 读取caps.json文件信息
    basis_capabilities: dict = load_file(capabilities_absolute_path, 'load_caps')

    capabilities = {}
    for key, value in basis_capabilities.items():
        if key in ["caps", "appium_server_ports"]:
            capabilities[key] = value

    if not capabilities["caps"].get('appPackage') or not isinstance(capabilities["caps"].get('appPackage'), str):
        raise

    if not capabilities["caps"].get('appActivity') or not isinstance(capabilities["caps"].get('appActivity'), str):
        raise

    return capabilities


def load_capabilities(work_path):
    # 加载配置信息
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
            port += 2
            _get_port(port)
    return port


def get_devices_ports(appium_port=4723, ports_num=1):
    # 获取两个可用的端口，做device实例启动的参数
    # bootstart_port会比appium_port大
    i = 0
    device_ports = []
    logger.debug("----生成可用appium server端口----\n")
    appium_port_msg = "appium server使用端口：\n"
    while len(device_ports) < ports_num:
        appium_port = _get_port(appium_port + i)
        bootstrap_port = _get_port(appium_port + 1)
        device_port = {
            "appium_port": appium_port,
            "bootstrap_port": bootstrap_port
        }
        appium_port_msg += f"appium_port:{appium_port}\n" \
                           f"bootstrap_port:{bootstrap_port}\n"
        device_ports.append(device_port)
        i += 2
    logger.debug(appium_port_msg)
    return device_ports


if __name__ == '__main__':
    pase_capabilities("./../examples")