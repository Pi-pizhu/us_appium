import os
import subprocess

from loguru import logger


class AndroidDebugBridge:

    """adb脚本
    1.获取设备id
    2.文件导入
    3.文件导出
    """

    def get_devices(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).stdout.readlines()
        for item in result:
            t = item.decode().split("\tdevice")
            if len(t) >= 2:
                devices.append(t[0])
        if len(devices) ==0 :
            raise ("无有效设备可连接")
        return devices

    def restart_device(self, device=None):
         subprocess.Popen("adb -s %s reboot" % (device), shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    def file_push(self, file_path, store_path):
        """
        导入文件
        :param file_path: 电脑文件路径
        :param store_path: 设备存放路径
        :return:
        """
        if not os.path.exists(file_path):
            logger.error(f"文件路径不存在：{file_path}\n")
            raise Exception(f"文件路径不存在：{file_path}")
        try:
            os.system(f"adb push {file_path} {store_path}")
        except Exception as error:
            logger.error(
                f"导入文件失败：{error}\n "
                f"导入文件：{file_path}\n")

    def file_pull(self, file_path, store_path):
        """
        导出文件
        :param file_path: 设备文件路径
        :param store_path: 电脑存放路径
        :return:
        """
        if not os.path.exists(store_path):
            logger.error(f"文件夹路径不存在：{store_path}\n")
            raise Exception(f"文件夹路径不存在：{store_path}")
        try:
            os.system(f"adb pull {file_path} {store_path}")
        except Exception as error:
            logger.error(f"导出文件失败：{error}\n "
                         f"导出文件：{file_path}\n")


if __name__ == '__main__':
    adb = AndroidDebugBridge()
    # print(os.system("source ~/.bash_profile"))
    # print(os.system("adb devices"))
    # print(os.system("adb --version"))
    print(adb.get_devices())