import json
import os
from loguru import logger
from base.file_plugin import load_file, locate_file


class TestCaps:
    """
    多进程加载，测试配置文件锁生效
    """

    def setup(self):
        self.file_path = locate_file(os.getcwd(), "examples/capabilities.json")

    def test_load_caps(self):
        caps = load_file(self.file_path, load_type="load_caps")
        logger.info(caps)

    def test_load_caps2(self):
        caps = load_file(self.file_path, load_type="load_caps")
        logger.info(caps)

    def teardown(self):
        msg = {
            "emult-5454": {
                "using_state": "no",
                "caps": {
                    "appPackage": "com.xueqiu.android",
                    "appActivity": ".view.WelcomeActivityAlias",
                    "app": "/Users/yewenkai/PycharmProjects/us_appium/apk/com.xueqiu.android_12.18.1_280.apk"
                }
            },
            "emult-5555": {
                "using_state": "no",
                "caps": {
                    "appPackage": "com.xueqiu.android",
                    "appActivity": ".view.WelcomeActivityAlias",
                    "app": "/Users/yewenkai/PycharmProjects/us_appium/apk/com.xueqiu.android_12.18.1_280.apk"
                }
            }
        }
        # msg = json.dumps(msg)
        with open(self.file_path, 'w') as caps_file:
            json.dump(msg, caps_file)
