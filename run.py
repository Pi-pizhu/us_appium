import argparse
import json
import os
from datetime import datetime
import pytest
import config
from base.BaseAdb import AndroidDebugBridge
from base.BasePhoneInfo import PhoneInfo
from base.make import initialize_dir
from base.mobile_core import get_devices_ports
from loguru import logger
from base.file_plugin import mkdir_dir, load_file, get_all_subdirectories, locate_file


def ensure_path_sep(path):
    """ ensure compatibility with different path separators of Linux and Windows
    """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return main_make(path)


def main_make(tests_paths):
    return os.path.abspath(tests_paths)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名、类名、方法名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', action="append", type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-n', '--procenum', help='多进程启动数量', type=int)
    extra_kwargs = {}
    test_paths = []
    parser_args = parser.parse_args()
    work_path = os.getcwd()
    if parser_args.dir:

        for test_dir in parser_args.dir:
            test_path = ensure_path_sep(test_dir)
            test_paths.append(test_path)
        work_path = test_paths[0]
        extra_kwargs["-d"] = test_paths
    if parser_args.keyword:
        extra_kwargs["-k"] = parser_args.keyword
    if parser_args.markexpr:
        extra_kwargs["-m"] = parser_args.markexpr
    if parser_args.reruns:
        extra_kwargs["-r"] = parser_args.reruns
    if parser_args.lf:
        extra_kwargs["-lf"] = parser_args.lf
    if parser_args.procenum:
        extra_kwargs["-n"] = parser_args.n

    try:
        work_path = locate_file(work_path, "settings.ini")
        work_path = os.path.dirname(work_path)
    except Exception as error:
        err_msg = f"工作路径：{work_path}"
        logger.error(f"{err_msg}\nsettings.ini文件不存在，它必须存在用于配置基础信息：{error}")
        raise (f"settings.ini文件不存在，它必须存在用于配置基础信息：{error}")

    try:
        test_abs_files = []
        for test_path in test_paths:
            test_abs_file = locate_file(work_path, test_path)
            test_abs_files.append(test_abs_file)
        extra_kwargs["-d"] = test_abs_files
    except Exception as error:
        err_msg = f"测试路径：{test_paths}\n"
        err_msg += f"工作路径：{work_path}\n"
        logger.error(f"{err_msg}\n指定的文件绝对路径错误：{error}")
        raise (f"指定的文件绝对路径错误：{error}")

    main(work_path, extra_kwargs)


def main(work_test_path, extra_kwargs: dict):
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
    # work_test_path = '/Users/yewenkai/PycharmProjects/us_appium/examples'
    # 获取当前时间
    specific_time = datetime.now().strftime("%Y%m%d%H%M%S")

    ini_dirs = initialize_dir(work_test_path)

    # 初始化logger日志文件
    log_file = os.path.join(ini_dirs["work_tests_log"], f"{specific_time}.run.main.log")
    logger.add(log_file)

    # 生成allure2日志报告存放路径
    allure2_report_path = mkdir_dir(work_test_path, "allure_report")

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
    settings_file = os.path.join(work_test_path, "settings.ini")
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
    if extra_kwargs.get("-n"):
        proc_num = extra_kwargs.pop("-n")
    else:
        proc_num = 1

    # 获取实际启动进程的数量，需要进行判断。以proc_num为主
    start_num = proc_num if proc_num < len(devices) else len(devices)
    logger.info("启动进程数量为：%s \n" % start_num)

    # 获取ports
    appium_ports = get_devices_ports(appium_port=appium_server_port, ports_num=start_num)

    # 根据启动进程数量来加载设备数,顺序加载

    devices_info = {}
    for i in range(start_num):
        phoneinfo = PhoneInfo('android', devices[i]).get_device_info()
        device_info = (phoneinfo)
        device_info['device_id'] = devices[i]

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
    temporary_caps_file = os.path.join(work_test_path, "capabilities.json")
    with open(temporary_caps_file, "w") as caps_file:
        json.dump(devices_info, caps_file)
    # +"/test_main.py::TestMain::test_article_action"
    cmd = ["-v"]
    if start_num > 1:
        cmd.append(f"-n={start_num}")

    cmd.append(f"--alluredir={allure2_report_path}")
    for key, value in extra_kwargs.items():
        if key == "-d":
            cmd.extend(value)
            continue
        cmd.append(f"{key}={value}")
    pytest.main(cmd)
    # allure生成报告的路径
    allure_html_file = os.path.join(work_test_path, "allure_html_report")
    os.system(f"allure generate {allure2_report_path} -o {allure_html_file} --clean")


if __name__ == '__main__':
    # extra_kwargs = {
    #     "-d": ["examples/test_main.py"]
    # }
    # work_test_path = "/Users/yewenkai/PycharmProjects/us_appium/examples"
    # main(work_test_path, extra_kwargs)
    cli()
    print("运行结束")