from appium.webdriver.common.mobileby import MobileBy
from base.driver_base import DriverBase


class PublicPage(DriverBase):

    _trading_page = {
        "step_type": "click",
        "local": "//*[@text='交易']",
        "position_type": MobileBy.XPATH,
    }

    def go_trading_page(self):
        self.step(**self._trading_page)
        return self