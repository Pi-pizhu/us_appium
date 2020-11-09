import os
import time

from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By

import config, config
from base.mobile_core import new_driver
from loguru import logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def step_retry(func):
    # 重试定位函数，可以用pytest重试替代
    def perform_func(self, *func_args, **func_kwargs):
        try:
            # todo:添加日志信息
            element_msg = func(self, *func_args, **func_kwargs)
            # 如果成功，当前重试次数清零
            self._current_retry_number = 0
            return element_msg
        except Exception as error:
            if self._current_retry_number == self._max_position_retry:
                # 抛出错误之前需要先截图
                self.screenshots()
                err_msg = "raise报错信息：%s \n" %error
                logger.error(err_msg)
                raise error
            self._current_retry_number += 1
            # todo：添加重试日志提示
            return func(self, *func_args, **func_kwargs)
    return perform_func


def exception_scene_recovery(func):
    # 异常场景恢复函数
    def perform_func(self, *func_args, **func_kwargs):
        try:
            # todo：添加定位日志信息
            step_msg = func(self, *func_args, **func_kwargs)
            # 如果成功，当前重试次数清零
            self._current_retry_number = 0
            return step_msg
        except Exception as error:
            if self._current_retry_number == self._max_position_retry:
                self.screenshots()
                err_msg = "raise报错信息：%s \n" % error
                logger.error(err_msg)
                raise("异常场景恢复失败：%s " %error)

            print(self._abnormal_bounding_box_information)
            print(type(self._abnormal_bounding_box_information))

            for locator_key, locator in self._abnormal_bounding_box_information.items():
                elements = self.finds(locator=locator)

                if len(elements) >= 1:
                    elements[0].click()
                    self._current_retry_number += 1
                    return func(self, *func_args, **func_kwargs)
            # 抛出错误之前需要先截图
            self.screenshots()
            err_msg = "raise报错信息：%s \n" % error
            logger.error(err_msg)
            raise error
    return perform_func


class DriverBase:
    _driver: WebDriver = None
    _url: str = None
    _touch_instance = None
    _wait_time = 20
    _sweep_frequency = 0.5
    _wait_type = None
    _max_position_retry = 3
    _current_retry_number = 0
    _screenshots_file = 'Screshots_img'
    # 因为tuple是不可变的数据类型，
    # 当装饰器exception_scene_recovery递减内部字典时，不会修改这个变量的内容
    _abnormal_bounding_box_information: dict = {
        "同意": (By.XPATH, "//*[@resource-id='com.xueqiu.android:id/tv_agree']")
    }


    def __init__(self, work_path=None, singleton=False):
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
        if not config.driver:
            pass
            # # 创建一个图片文件夹，用来装失败截图
            # curnt_path = os.path.abspath('.')
            # screshots_img_path = os.path.join(curnt_path, self._screenshots_file)
            # if not os.path.isdir(screshots_img_path):
            #     mkdir_file(curnt_path, self._screenshots_file)
            # current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            # work_screshots_img_path = mkdir_file(screshots_img_path, current_time+"_img")
            # config.screenshots_file = work_screshots_img_path
            #
            # # 设置配置信息
            # capabilities = pase_capabilities(work_path)
            # address = capabilities.get('address')
            # proxy = capabilities.get('proxy') if capabilities.get('proxy') else None
            # # 创建新的实例
            # self.driver = new_driver(address, capabilities)
            # config.driver = self.driver
            # self.driver.implicitly_wait(10)
        else:
            self.driver = config.driver

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @property
    def touch_instance(self):
        return self.touch_instance

    @touch_instance.setter
    def touch_instance(self, touch_instance):
        self._touch_instance = touch_instance

    @property
    def abnormal_bounding_box_information(self):
        return self._abnormal_bounding_box_information

    @abnormal_bounding_box_information.setter
    def abnormal_bounding_box_information(self, information):
        self._abnormal_bounding_box_information = information

    # @step_retry
    def find(self, locator, wait_time, sweep_frequency, wait_type):
        # 显示等待定位，加入失败重试机制
        element = self._wait(locator, "element", wait_time, sweep_frequency, wait_type)
        return element

    def finds(self, locator, wait_time=_wait_time, sweep_frequency=_sweep_frequency, wait_type=_wait_type) -> list:
        # 显示等待定位，加入失败重试机制
        elements = self._wait(locator, "elements", wait_time, sweep_frequency, wait_type)
        return elements

    def _wait(self, locator, element_type, wait_time, sweep_frequency, wait_type):
        """
        设置显示等待
        :param wait_time: 显示等待时长
        :param sweep_frequency: 扫描元素频率
        :param locator: 元素定位内容
        :param wait_type: 显示等待方式
        :return:
        """
        wait_element = WebDriverWait(self.driver, wait_time, sweep_frequency)

        if element_type == 'element':
        #     if wait_type == '':
        #         return wait_element.until(EC.presence_of_element_located(locator))
        #     elif wait_type == '':
        #         return wait_element.until(EC.invisibility_of_element(locator))
            return wait_element.until(EC.element_to_be_clickable(locator))
        else:
            return wait_element.until(EC.visibility_of_all_elements_located(locator))
        #     if wait_type == '':
        #         return wait_element.until(EC.presence_of_all_elements_located(locator))
        #     elif wait_type == '':
        #         return wait_element.until(EC.visibility_of_all_elements_located(locator))

    @exception_scene_recovery
    def step(self, step_type, local, position_type = By.XPATH, desc_information=None, wait_time = _wait_time, sweep_frequency = _sweep_frequency, wait_type = _wait_type):
        """

        :param step_type: action_type
        :param local: element_attribute
        :param position_type:
        :param desc_information:
        :param wait_time:
        :param sweep_frequency:
        :param wait_type:
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
                   f"元素定位方式：{wait_type}\n"
        logger.info(step_msg)

        if step_type == 'touchaction':
            self._touch_action(step_type, desc_information)
        else:
            element: WebElement = self.find(locator, wait_time, sweep_frequency, wait_type)

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
        if not self.touch_instance:
            touch_instance = TouchAction()
        else:
            touch_instance = self.touch_instance

        if step_type == 'press':
            touch_instance.press(desc_information)
        elif step_type == 'wait':
            touch_instance.wait(desc_information)
        elif step_type == 'longpress':
            touch_instance.long_press(desc_information)
        elif step_type == 'perform':
            touch_instance.perform()
        elif step_type == 'release':
            touch_instance.release()
        elif step_type == 'move':
            touch_instance.move_to(desc_information)
        elif step_type == 'tap':
            touch_instance.tap(desc_information)
        else:
            raise("没有对应的touch_action操作")

    def screenshots(self):
        # 应用截图功能，多用于报错时截图
        # path:执行用例的路径
        # time：图片的名称
        screenshots_file = config.screenshots_file
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        screenshots_path = os.path.join(screenshots_file,current_time)
        img_name = screenshots_path + ".png"
        self.driver.get_screenshot_as_file(img_name)

    def _get_page_contents(self):
        return self.driver.contexts

    def switch_contents(self, index):
        contents = self._get_page_contents()
        print(contents)
        self.driver.switch_to.context(contents[index])

if __name__ == '__main__':
    # a = time.time()
    a = time.strftime("%Y%m%d%H%M%S", time.localtime())
    print(a)
    print(type(a))
    print(os.getcwd())