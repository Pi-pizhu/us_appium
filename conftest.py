import pytest
import config
from base.BaseAppiumServer import AppiumServer
from base.mobile_core import new_driver


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action='store', help="devices info")


@pytest.fixture(scope='session', autouse=True)
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope='session', autouse=True)
def start_test(cmdopt):

    """
    生成driver实例需要条件：
    1.设备池：设备信息
    2.appium server：对应启动appium server端
    3.driver实例信息：配置信息、连接地址
    :return:
    """
    device_info = eval(cmdopt)
    # # 启动appium server
    appium_server = AppiumServer()

    driver_address = device_info.pop('driver_address')
    # 生成driver实例
    driver = new_driver(address=driver_address, capabilities=device_info)
    config.driver = driver
    driver.implicitly_wait(5)
    yield
    driver.quit()
    # appium_server.stop_server()