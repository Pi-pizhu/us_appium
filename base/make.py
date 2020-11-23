from datetime import datetime

from base.file_plugin import mkdir_dir


def initialize_dir(test_path):
    # 获取当前时间
    day_time = datetime.now().strftime("%Y%m%d")

    # 本次运行日志目录
    work_log_path = mkdir_dir(test_path, "log", day_time)
    # 测试 日志存放路径
    work_tests_log = mkdir_dir(work_log_path, "tests_log")
    # appium 日志存放路径
    work_appium_log = mkdir_dir(work_log_path, "appium_log")
    # 图片存放路径
    work_img_path = mkdir_dir(test_path, "img", day_time)
    return {
        "work_tests_log": work_tests_log,
        "work_appium_log": work_appium_log,
        "work_img_path": work_img_path,
        "work_log_path": work_log_path,
    }