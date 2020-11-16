import json
import os

from base.file_plugin import mkdir_file


class AllurePlugin:

    # 保存历史数据
    def save_history(self, history_dir, dist_dir):
        if not os.path.exists(os.path.join(dist_dir, "history")):
            mkdir_file(os.path.join(dist_dir, "history"))
        else:
            # 遍历报告report下allure-report下的history目录下的文件
            for file in os.listdir(os.path.join(dist_dir, "history")):
                old_data_dic = {}
                old_data_list = []
                # 1、从report下allure-report下的history目录下的文件读取最新的历史纪录
                with open(os.path.join(dist_dir, "history", file), 'rb') as f:
                    new_data = json.load(f)
                # 2、从Report下的history(历史文件信息存储目录)读取老的历史记录
                try:
                    with open(os.path.join(history_dir, file), 'rb') as fr:
                        old_data = json.load(fr)

                        if isinstance(old_data, dict):
                            old_data_dic.update(old_data)
                        elif isinstance(old_data, list):
                            old_data_list.extend(old_data)
                except Exception as fe:
                    print("{}文件查找失败信息：{}，开始创建目标文件！！！".format(history_dir, fe))
                    mkdir_file(os.path.join(history_dir, file))
                    # 3、合并更新最新的历史纪录到report下的history目录对应浏览器目录中
                with open(os.path.join(history_dir, file), 'w') as fw:
                    if isinstance(new_data, dict):
                        old_data_dic.update(new_data)
                        json.dump(old_data_dic, fw, indent=4)
                    elif isinstance(new_data, list):
                        old_data_list.extend(new_data)
                        json.dump(old_data_list, fw, indent=4)
                    else:
                        print("旧历史数据异常")

    # 导入历史数据
    def import_history_data(self, history_save_dir, result_dir):
        if not os.path.exists(history_save_dir):
            print("未初始化历史数据！！！进行首次数据初始化!!!")
        else:
            # 读取历史数据
            for file in os.listdir(history_save_dir):
                # 读取最新的历史纪录
                with open(os.path.join(history_save_dir, file), 'rb') as f:
                    new_data = json.load(f)
                # 写入目标文件allure-result中，用于生成趋势图
                mkdir_file(os.path.join(result_dir, "history", file))
                try:
                    with open(os.path.join(result_dir, "history", file), 'w') as fw:
                        json.dump(new_data, fw, indent=4)
                except Exception as fe:
                    print("文件查找失败信息：{}，开始创建目标文件".format(fe))