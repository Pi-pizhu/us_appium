import pytest

from page.trading_page import TradingPage
from page.public_page import PublicPage


class TestTrading:

    def setup(self):
        self.trading_page = TradingPage()
        # 切换到交易页面
        PublicPage().go_trading_page()

        # 确认锚点情况
        anchor = self.trading_page.confirm_anchor()
        assert anchor == "港美"

    def test_switch_contents(self):
        # 切换webview
        self.trading_page.switch_page_contents()


    def test_goto_a_stocks(self):
        self.trading_page.goto_a_stocks().back().click_a_stocks_jump().back()


    def test_goto_fund(self):
        self.trading_page.goto_fund().back().click_fund_jump().back()