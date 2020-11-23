from appium.webdriver.common.mobileby import MobileBy

from base.driver_base import DriverBase


class MainPage(DriverBase):

    _abnormal_bounding_box_information = {
        "同意": (MobileBy.XPATH, "//*[@resource-id='com.xueqiu.android:id/tv_agree']")
    }

    # _recommended = {
    #     "step_type": "attribute",
    #     "local": "//*[@resource-id='com.xueqiu.android:id/title_text' and @text='推荐']",
    #     "position_type": MobileBy.XPATH,
    #     "desc_information": "text"
    # }

    _posotion_element = {
        "step_type": "attribute",
        "local": "//*[@text='关注']",
        "position_type": MobileBy.XPATH,
        "desc_information": "text"
    }

    # 通用按钮
    # 返回按钮
    _back_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/action_back']",
        "position_type": MobileBy.XPATH
    }

    # 关闭按钮
    _close_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/iv_close']",
        "position_type": MobileBy.XPATH
    }

#################################
    # 搜索按钮：上滑后变成搜索按钮
    _search_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/action_search']",
        "position_type": MobileBy.XPATH
    }

    # 搜索框
    _search_box = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/home_search']",
        "position_type": MobileBy.XPATH
    }
#################################
    # 首页顶部分类
    # 关注
    _attention = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/title_container']/android.widget.FrameLayout[1]",
        "position_type": MobileBy.XPATH
    }
    # 推荐
    _recommended = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/title_container']/android.widget.FrameLayout[2]",
        "position_type": MobileBy.XPATH
    }

    # 热门
    _hot = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/title_container']/android.widget.FrameLayout[3]",
        "position_type": MobileBy.XPATH
    }

    # pk赛
    _pk = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/title_container']/android.widget.FrameLayout[4]",
        "position_type": MobileBy.XPATH
    }

    # 消息
    _message = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/action_message']",
        "position_type": MobileBy.XPATH
    }
#################################
    # 7*24 热门
    # 7*24 logo
    _hot_logo = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/news_logo']",
        "position_type": MobileBy.XPATH
    }

    # 7*24 热门
    _hot_message = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/splash_text_tv']",
        "position_type": MobileBy.XPATH
    }
#################################
    # 雪球热股榜

    # 热股榜返回
    _hot_back_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/back']",
        "position_type": MobileBy.XPATH
    }

    # 热股榜 全部
    _hot_all_stocks = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/all_stock_tv']",
        "position_type": MobileBy.XPATH
    }

    # 热股榜 窗口1 四家公司 左半边
    _hot_stocks_one = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_one']",
        "position_type": MobileBy.XPATH
    }

    _hot_stocks_two = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_two']",
        "position_type": MobileBy.XPATH
    }

    _hot_stocks_three = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_three']",
        "position_type": MobileBy.XPATH
    }

    _hot_stocks_four = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_four']",
        "position_type": MobileBy.XPATH
    }

    # 热股榜 窗口2 三家公司 右半边
    _hot_stocks_five = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_five']",
        "position_type": MobileBy.XPATH
    }

    _hot_stocks_six = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_six']",
        "position_type": MobileBy.XPATH
    }

    _hot_stocks_seven = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/stock_seven']",
        "position_type": MobileBy.XPATH
    }
#################################
    # 热门话题
    # 话题返回
    _topic_back_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/tv_action_back']",
        "position_type": MobileBy.XPATH
    }

    _topic_msg_back_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/transparent_action_back']",
        "position_type": MobileBy.XPATH
    }

    # 全部
    _hot_all_topic = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/hot_topic_all']",
        "position_type": MobileBy.XPATH
    }

    # 话题1
    _hot_topic_one = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/hot_topic_rv']/android.widget.LinearLayout[1]//android.widget.ImageView",
        "position_type": MobileBy.XPATH
    }

    # 话题2
    _hot_topic_two = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/hot_topic_rv']/android.widget.LinearLayout[2]//android.widget.ImageView",
        "position_type": MobileBy.XPATH
    }
#################################
    # 推荐分类
    # 推荐分类 banner
    # banner 切换icon
    _recommended_banner_icon = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/banner_indicator_container']/android.widget.ImageView[icon_index]",
        "position_type": MobileBy.XPATH
    }

    # banner
    _recommended_banner = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/head_banner_img']",
        "position_type": MobileBy.XPATH
    }
#################################
    # 推荐文章 作者头像
    _recommended_author_portrait = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/profileImage']",
        "position_type": MobileBy.XPATH
    }

    # 推荐文章 作者名字 发表时间 一栏
    _recommended_author_name = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/name_layout']",
        "position_type": MobileBy.XPATH
    }

    # 推荐文章内容
    _recommended_article_text = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/status_container']",
        "position_type": MobileBy.XPATH
    }

    # 推荐文章 转发按钮
    _recommended_article_retweet = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/retweet_count_view']/android.widget.ImageView",
        "position_type": MobileBy.XPATH
    }

    # 推荐文章 评论按钮
    _recommended_article_comment = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/comment_count_view']/android.widget.ImageView",
        "position_type": MobileBy.XPATH
    }

    # 推荐文章 点赞按钮
    _recommended_article_reward = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/reward_count_view']/android.widget.ImageView",
        "position_type": MobileBy.XPATH
    }

    # 右下角 编写文章按钮
    _recommended_write_article = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/post_status']",
        "position_type": MobileBy.XPATH
    }

    # 关注
    # 去看看
    _empty_btn = {
        "step_type": "click",
        "local": "//*[@resource-id='com.xueqiu.android:id/empty_button']",
        "position_type": MobileBy.XPATH
    }

    # 获取设备屏幕信息
    def get_size(self):
        size = self.driver.get_window_size()
        self.width = size['width']
        self.height = size['height']
        return self

    def slide(self):
        # 上滑
        x = self.width / 2
        y = int(self.height * 0.8)
        after_y = int(self.height * 0.2)
        self.driver.swipe(start_x=x, start_y=y, end_x=x, end_y=after_y)
        return self

    # 获取锚点信息
    def confirm_anchor(self):
        return self.step(**self._posotion_element)

    # 定义通用功能 ############################
    # 返回
    def back(self):
        self.step(**self._back_btn)
        return self

    # 关闭
    def close(self):
        self.step(**self._close_btn)
        return self

    # 首页分类 ############################
    def goto_attention(self):
        self.step(**self._attention)
        return self

    def goto_recommended(self):
        self.step(**self._recommended)
        return self

    def goto_hot(self):
        self.step(**self._hot)
        return self

    def goto_pk(self):
        self.step(**self._pk)
        return self

    def goto_message(self):
        self.step(**self._message)
        return self

    # 热门分类 相关内容 ############################
    def click_hot_logo(self):
        self.step(**self._hot_logo)
        return self

    def click_hot_message(self):
        self.step(**self._hot_message)
        return self

    # 热股榜 相关内容
    def hot_back_btn(self):
        self.step(**self._hot_back_btn)
        return self

    def goto_hot_all_stocks(self):
        self.step(**self._hot_all_stocks)
        return self

    def goto_hot_stock_one(self):
        self.step(**self._hot_stocks_one)
        return self

    def goto_hot_stock_two(self):
        self.step(**self._hot_stocks_two)
        return self

    def goto_hot_stock_three(self):
        self.step(**self._hot_stocks_three)
        return self

    def goto_hot_stock_four(self):
        self.step(**self._hot_stocks_four)
        return self

    def goto_hot_stock_five(self):
        self.step(**self._hot_stocks_five)
        return self

    def goto_hot_stock_six(self):
        self.step(**self._hot_stocks_six)
        return self

    def goto_hot_stock_seven(self):
        self.step(**self._hot_stocks_seven)
        return self

    # 热门话题
    def topic_back_btn(self):
        self.step(**self._topic_back_btn)
        return self

    def goto_hot_all_topic(self):
        self.step(**self._hot_all_topic)
        return self

    def topic_msg_back_btn(self):
        self.step(**self._topic_msg_back_btn)
        return self

    def click_hot_topic_one(self):
        self.step(**self._hot_topic_one)
        return self

    def click_hot_topic_two(self):
        self.step(**self._hot_topic_two)
        return self

    # 推荐分类 ############################
    # 选择banner下标
    def choose_recommended_banner_icon(self, icon_index=1):
        if icon_index < 1 or icon_index > 5:
            raise("请在1-5之间选择")

        _recommended_banner_icon = self._recommended_banner_icon
        _recommended_banner_icon["local"] = _recommended_banner_icon["local"].replace("icon_index", str(icon_index))
        self.step(**_recommended_banner_icon)
        return self
    # 点击banner
    def click_recommended_banner(self):
        self.step(**self._recommended_banner)
        return self

    # 推荐文章 点击作者头像
    def click_recommended_author_portrait(self):
        self.step(**self._recommended_author_portrait)
        return self

    def click_recommended_author_name(self):
        self.step(**self._recommended_author_name)
        return self

    def click_recommended_article_text(self):
        self.step(**self._recommended_article_text)
        return self

    def click_recommended_article_retweet(self):
        self.step(**self._recommended_article_retweet, elements_index=1)
        return self

    def click_recommended_article_comment(self):
        self.step(**self._recommended_article_comment, elements_index=1)
        return self

    def click_recommended_article_reward(self):
        self.step(**self._recommended_article_reward, elements_index=1)
        return self

    def goto_recommended_write_article(self):
        self.step(**self._recommended_write_article)
        return self

    # 关注分类 相关内容 ############################
    def goto_empty_btn(self):
        self.step(**self._empty_btn)
        return self