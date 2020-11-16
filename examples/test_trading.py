import os
from loguru import logger

from page.trading_page import TradingPage
from page.public_page import PublicPage


class TestTrading:

    def setup(self):
        work_path = os.path.split(os.path.realpath(__file__))[0]
        self.trading_page = TradingPage(work_path)
        # 切换到交易页面
        PublicPage(work_path).go_trading_page()
        logger.debug(f"test_trading.py 当前运行进程为：{os.getpid()}")

        # 确认锚点情况
        anchor = self.trading_page.confirm_anchor()
        assert anchor == "港美"

    def test_switch_contents(self):
        # 切换webview
        self.trading_page.switch_page_contents()


    def test_goto_a_stocks(self):
        self.trading_page.goto_a_stocks().back().click_a_stocks_jump().back()
    #
    #
    # def test_goto_fund(self):
    #     self.trading_page.goto_fund().back().click_fund_jump().back()