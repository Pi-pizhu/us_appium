import os
from loguru import logger

from page.main_page import MainPage
from page.public_page import PublicPage


class TestMain:

    def setup_class(self):
        work_path = os.path.split(os.path.realpath(__file__))[0]
        # work_path = os.getcwd()
        self.main_page = MainPage(work_path)
        self.public_page = PublicPage(work_path)
        logger.debug(f"test_main.py 当前运行进程为：{os.getpid()}")
        anchor = self.main_page.confirm_anchor()
        assert anchor == "关注"

    def teardown(self):
        self.main_page.start_activity()

    def test_switch_class(self):
        self.main_page.goto_attention().goto_recommended().goto_hot().goto_pk()

# class TestMainHot:

    def test_hot_day(self):
        self.main_page.goto_hot().click_hot_logo().back().click_hot_message().back()

    def test_hot_stocks(self):
        self.main_page.goto_hot().goto_hot_all_stocks().hot_back_btn().goto_hot_stock_one().back()\
            .goto_hot_stock_two().back().goto_hot_stock_three().back().goto_hot_stock_four().back()\
            .goto_hot_stock_five().back().goto_hot_stock_six().back().goto_hot_stock_seven().back()

    def test_hot_topic(self):
        self.main_page.goto_hot().goto_hot_all_topic().topic_back_btn().click_hot_topic_one()\
            .topic_msg_back_btn().click_hot_topic_two().topic_msg_back_btn()

# class TestMainRecommended:

    def test_recommended_banner(self):
        self.main_page.goto_recommended()
        banner_icon_index = 1
        while banner_icon_index < 6:
            self.main_page.choose_recommended_banner_icon(banner_icon_index)\
                .click_recommended_banner().back()
            banner_icon_index += 1

    def test_article_content(self):
        self.main_page.goto_recommended().click_recommended_author_portrait().back()\
            .click_recommended_author_name().back().click_recommended_article_text().back()

    def test_article_action(self):
        self.main_page.goto_recommended().get_size().slide().click_recommended_article_retweet()\
            .close().click_recommended_article_comment().back()\
            .click_recommended_article_reward().close()


# class TestMainAttention:

    def test_empty(self):
        self.main_page.goto_empty_btn().back()

    def teardown_class(self):
        self.main_page.quit()