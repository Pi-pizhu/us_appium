import os
import subprocess


class AndroidDebugBridge:

    """adb脚本
    1.获取设备id
    2.重启设备
    3.文件导入
    4.文件导出
    5.打开指定app
    6.根据包名获取进程id
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

    def file_push(self, file):
        pass

    def file_pull(self):
        pass

    def open_app(self):
        pass

    def get_app_pid(self):
        pass


if __name__ == '__main__':
    adb = AndroidDebugBridge()
    # print(os.system("source ~/.bash_profile"))
    # print(os.system("adb devices"))
    # print(os.system("adb --version"))
    print(adb.get_devices())