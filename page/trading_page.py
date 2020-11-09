from appium.webdriver.common.mobileby import MobileBy

from base.driver_base import DriverBase


class TradingPage(DriverBase):

    _abnormal_bounding_box_information = {}

    # 通过锚点 确定页面情况 获取到 港美 text
    _posotion_element = {
        "step_type": "attribute",
        "local": "//*[@resource-id='com.xueqiu.android:id/title_container']/android.widget.FrameLayout[1]/com.xueqiu.android:id/title_text",
        "position_type": MobileBy.XPATH,
        "desc_information": "text"
    }

    # 通用按钮
    # 返回按钮
    _back_btn = {
        "step_type": "click",
        "local": "//*[@class='android.widget.ImageButton']",
        "position_type": MobileBy.XPATH
    }

    # A股开户
    _a_stocks = {
        "step_type": "click",
        "local": "//*[@resource-id='//*[@class='trade_home_agu_3bZ']/trade_home_info_205']",
        "position_type": MobileBy.XPATH
    }

    # A股开户跳转
    _a_stocks_jump = {
        "step_type": "click",
        "local": "//*[@resource-id='//*[@class='trade_home_agu_3bZ']/trade_home_iconArrow_fMa']",
        "position_type": MobileBy.XPATH
    }

    # 基金开户
    _fund = {
        "step_type": "click",
        "local": "//*[@resource-id='//*[@class='trade_home_danjuan_23L']/trade_home_info_205']",
        "position_type": MobileBy.XPATH
    }

    # 基金开户跳转
    _fund_jump = {
        "step_type": "click",
        "local": "//*[@resource-id='//*[@class='trade_home_danjuan_23L']/trade_home_iconArrow_fMa']",
        "position_type": MobileBy.XPATH
    }

    def confirm_anchor(self):
        return self.step(**self._posotion_element)

    # 切换到webview
    def switch_page_contents(self, index=-1):
        self.switch_contents(index)
        return self

    def goto_a_stocks(self):
        self.step(**self._a_stocks)
        return self

    def click_a_stocks_jump(self):
        self.step(**self._a_stocks_jump)
        return self

    def goto_fund(self):
        self.step(**self._fund)
        return self

    def click_fund_jump(self):
        self.step(**self._fund_jump)
        return self

    def back(self):
        self.step(**self._back_btn)
        return self

