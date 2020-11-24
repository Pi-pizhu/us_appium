import os, json
import time
from datetime import datetime

from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By

import config
from base.BaseAdb import AndroidDebugBridge
from base.BaseAppiumServer import AppiumServer
from base.make import initialize_dir
from base.mobile_core import new_driver, load_capabilities
from loguru import logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.file_plugin import load_file


def exception_scene_recovery(func):
    # 异常场景恢复函数
    def perform_func(self, *func_args, **func_kwargs):
        try:
            # TODO：添加定位日志信息
            step_msg = func(self, *func_args, **func_kwargs)
            # 如果成功，当前重试次数清零
            self._current_retry_number = 0
            return step_msg
        except Exception as error:
            # todo: 错误日志 太难定位
            err_msg = json.dumps(func_kwargs) + "\n"
            if self._current_retry_number == self._max_position_retry:
                self.screenshots()
                err_msg += "raise报错信息：%s \n" % error
                logger.error(err_msg)
                raise("异常场景恢复失败：%s " %error)

            for locator_key, locator in self._abnormal_bounding_box_information.items():
                # todo: 查找失败时 直接就抛出异常了 并没有循环重试
                elements = self._wait(locator=locator, wait_time=func_kwargs["wait_time"],
                                     search_type=func_kwargs["search_type"], sweep_frequency=func_kwargs["sweep_frequency"],
                                     element_type='elements')

                if len(elements) >= 1:
                    elements[0].click()
                    self._current_retry_number += 1
                    return func(self, *func_args, **func_kwargs)
            # 抛出错误之前需要先截图
            self.screenshots()
            err_msg += "raise报错信息：%s \n" % error
            logger.error(err_msg)
            # todo: 添加错误截图
            raise error
    return perform_func


class DriverBase:
    _driver: WebDriver = None
    _url: str = None
    _touch_instance = None
    _wait_time = 20
    _sweep_frequency = 0.5
    _search_type = None
    _max_position_retry = 3
    _current_retry_number = 0
    _screenshots_path = 'Screshots_img'
    _adb_instance = None
    # 因为tuple是不可变的数据类型，
    # 当装饰器exception_scene_recovery递减内部字典时，不会修改这个变量的内容
    _abnormal_bounding_box_information: dict = {
        "同意": (By.XPATH, "//*[@resource-id='com.xueqiu.android:id/tv_agree']")
    }

    def __init__(self, test_work_path):
        """
        初始化：
        1.获取设备信息
        2.启动appium server服务
        3.创建driver实例
            以上需要共享port端口，device_id,或是在config.py中生成

        需要创建当次运行时存放截图的文件夹
        需要获取当次运行用例时的目录路径
        需要获取配置
        如果是多设备运行，需要动态获取deviceName、动态开启多个appium端口，并行运行
        单个设备用例需要多线程并发运行。
        :param work_path:
        :param singleton:
        """
        if not getattr(config, "driver", None):
            # 初始化logger文件
            ini_dirs = initialize_dir(test_work_path)
            specific_time = datetime.now().strftime("%Y%m%d%H%M%S")

            logger.add(ini_dirs["work_tests_log"] + f"/{specific_time}.run.log")
            logger.info(f"当前进程为：{os.getpid()} \n")
            logger.info(f"父进程为：{os.getppid()} \n")
            logger.info("工作路径：%s \n" % test_work_path)
            logger.debug(f"driverbase——os.getcwd()：{os.getcwd()}")
            # 设置图片存放路径
            self._screenshots_path = ini_dirs["work_img_path"]

            # 加载caps配置信息
            capabilities = load_capabilities(test_work_path)
            appium_ports = capabilities["appium_server_ports"]
            info_log_msg = f"caps配置信息为：{json.dumps(capabilities)} \n"

            appium_address = capabilities["host"]

            # 处理appium 配置信息
            appium_log_file = os.path.join(ini_dirs["work_appium_log"], f"{specific_time}_appium.log")
            info_log_msg += f"appium log日志文件为：{appium_log_file} \n"

            logger.info(info_log_msg)
            # 启动appium server
            self.appium_server = AppiumServer()
            # 配置信息
            self.appium_server.start_server(appium_address=appium_address,
                                       appium_port=appium_ports['appium_port'],
                                       bootstrap_port=appium_ports['bootstrap_port'],
                                       appium_log_file=appium_log_file)
            # 初始化driver实例
            self.driver = new_driver(appium_address, appium_ports['appium_port'], capabilities["caps"])
            config.driver = self.driver
            self._appPackage = capabilities["caps"]["appPackage"]
            self._appActivity = capabilities["caps"]["appActivity"]

        else:
            self.driver = config.driver
        self.driver.implicitly_wait(5)

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @property
    def touch_instance(self):
        if not self._touch_instance:
            self._touch_instance = TouchAction()
        return self._touch_instance

    @property
    def adb_instance(self):
        if not self._adb_instance:
            self._adb_instance = AndroidDebugBridge()
        return self._adb_instance

    @property
    def abnormal_bounding_box_information(self):
        return self._abnormal_bounding_box_information

    @abnormal_bounding_box_information.setter
    def abnormal_bounding_box_information(self, information):
        self._abnormal_bounding_box_information = information

    @exception_scene_recovery
    def find(self, locator, wait_time, sweep_frequency, search_type, element_type='element'):
        # 显示等待定位，加入失败重试机制
        element = self._wait(locator, element_type, wait_time, sweep_frequency, search_type)
        return element

    # def finds(self, locator, wait_time=_wait_time, sweep_frequency=_sweep_frequency, search_type=_search_type) -> list:
    #     # 显示等待定位，加入失败重试机制
    #     elements = self._wait(locator, "elements", wait_time, sweep_frequency, search_type)
    #     return elements

    def _wait(self, locator, element_type, wait_time, sweep_frequency, search_type):
        """
        设置显示等待
        :param wait_time: 显示等待时长
        :param sweep_frequency: 扫描元素频率
        :param locator: 元素定位内容
        :param search_type: 查找的方式 可见时查找 或者 渲染时查找
        :return:
        """
        wait_element = WebDriverWait(self.driver, wait_time, sweep_frequency)

        if element_type == 'element':
            return wait_element.until(EC.element_to_be_clickable(locator))
        else:
            return wait_element.until(EC.visibility_of_all_elements_located(locator))

    def step(self, step_type, local, position_type = By.XPATH, desc_information=None,
             wait_time = _wait_time, sweep_frequency = _sweep_frequency,
             search_type = _search_type, elements_index=None):
        """

        :param step_type: action_type
        :param local: element_attribute
        :param position_type:
        :param desc_information:
        :param wait_time:
        :param sweep_frequency:
        :param search_type:
        :return:
        """
        logger.info("----进入元素操作----\n")
        step_type = step_type.lower()
        if local and isinstance(local, str):
            locator = (
                position_type,
                local
            )
        else:
            logger.error("元素定位信息不正确，请重新输入元素定位信息")
            raise("元素定位信息不正确，请重新输入元素定位信息")

        step_msg = f"操作类型：{step_type}\n" \
                   f"元素信息：{locator}\n" \
                   f"额外信息：{desc_information}\n" \
                   f"等待时间：{wait_time}\n" \
                   f"扫描频率：{sweep_frequency}\n" \
                   f"元素定位方式：{search_type}\n"
        logger.info(step_msg)

        if step_type == 'touchaction':
            self._touch_action(step_type, desc_information)
        else:
            if not elements_index:
                element: WebElement = self.find(
                    locator=locator, wait_time=wait_time,
                    sweep_frequency=sweep_frequency,
                    search_type=search_type)
            else:
                element: WebElement = self.find(
                    locator=locator, wait_time=wait_time,
                    sweep_frequency=sweep_frequency,
                    search_type=search_type, element_type="elements")[elements_index]

            if step_type in ("send", "attribute") and not desc_information:
                raise("对应元素操作：%s, 需要搭配描述信息: desc_information" %step_type)

            if step_type == 'click':
                element.click()
            elif step_type == 'send':
                element.send_keys(desc_information)
            elif step_type == 'attribute':
                return element.get_attribute(desc_information)
            elif step_type == 'submit':
                element.submit()
            elif step_type == 'clear':
                element.clear()
            elif step_type == 'driver':
                return self.driver

    def _touch_action(self, step_type, desc_information=None):
        if step_type == 'press':
            self.touch_instance.press(desc_information)
        elif step_type == 'wait':
            self.touch_instance.wait(desc_information)
        elif step_type == 'longpress':
            self.touch_instance.long_press(desc_information)
        elif step_type == 'perform':
            self.touch_instance.perform()
        elif step_type == 'release':
            self.touch_instance.release()
        elif step_type == 'move':
            self.touch_instance.move_to(desc_information)
        elif step_type == 'tap':
            self.touch_instance.tap(desc_information)
        else:
            raise("没有对应的touch_action操作")

    def screenshots(self):
        # 应用截图功能，多用于报错时截图
        # path:执行用例的路径
        # time：图片的名称
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        screenshots_file = os.path.join(self._screenshots_path, f'{current_time}.png')
        self.driver.get_screenshot_as_file(screenshots_file)

    def _get_page_contents(self):
        return self.driver.contexts

    def switch_contents(self, index):
        contents = self._get_page_contents()
        print(contents)
        self.driver.switch_to.context(contents[index])

    def quit(self):
        # 测试结束后 关闭appium server 以及 driver
        logger.info("关闭driver和server")
        self.driver.quit()
        self.appium_server.stop_server()

    def start_activity(self):
        # 启动app到指定activity上
        self.driver.start_activity(app_package=self._appPackage, app_activity=self._appActivity)

    def file_push(self, file_path, store_path):
        # 文件导入
        self.adb_instance.file_push(file_path, store_path)

    def file_pull(self, file_path, store_path):
        # 文件导出
        self.adb_instance.file_pull(file_path, store_path)

if __name__ == '__main__':
    # a = time.time()
    a = time.strftime("%Y%m%d%H%M%S", time.localtime())
    print(a)
    print(type(a))
    print(os.getcwd())