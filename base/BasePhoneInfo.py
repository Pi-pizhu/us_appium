import os
import re
import subprocess
from loguru import logger

"""设备信息获取Android/IOS
1.获取设备品牌
2.获取设备型号
3.获取设备名
4.获取设备系统版本
5.获取设备分辨率
6.获取设备最大内存
7.获取设备CPU核数
8.获取设备当前剩余内存
"""


def eliminate_special_symbols(func):
    def perform_func(*args, **kwargs):
        results: str = func(*args, **kwargs)
        return results.replace('\n', '') if results else None
    return perform_func


def eliminate_blank_space(func):
    def perform_func(*args, **kwargs):
        results: str = func(*args, **kwargs)
        return results.replace(' ', '') if results else None
    return perform_func


class AndroidInfo:

    _device_id = None

    def __init__(self, device_id):
        self.device_id = device_id

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        # Lock.acquire()
        self._device_id = device_id
        # Lock.release()

    def us_cmd(self, cmd):
        # results = os.system("adb " + cmd)
        results = subprocess.Popen("adb " + cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE).stdout.readlines()
        return results

    @eliminate_special_symbols
    def get_device_brand(self) ->str :
        # 获取设备品牌
        cmd = "-s %s shell getprop ro.product.brand" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        return results.decode()

    # def get_mobile_system_information(self, devices_id):
    #     # Android获取手机系统版本
    #     adb_commod = "adb -d -s " + devices_id + " shell getprop ro.build.version.release "
    #     devices_system_data = os.popen(adb_commod)
    #     devices_system_msg = devices_system_data.read()
    #     devices_system_data.close()
    #     return float(devices_system_msg)

    @eliminate_special_symbols
    def get_model_device(self) ->str :
        # 获取设备型号
        cmd = "-s %s shell getprop ro.product.model" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        return results.decode()

    @eliminate_special_symbols
    def get_device_name(self) ->str :
        # 获取设备名称
        cmd = "-s %s shell getprop ro.product.device" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        return results.decode()

    @eliminate_special_symbols
    def get_device_system_version(self) ->str :
        # 获取系统版本
        cmd = "-s %s shell getprop ro.build.version.release" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        return results.decode()

    @eliminate_blank_space
    def get_device_resolution(self) ->str :
        # 获取设备分辨率
        # 高通平台
        cmd = "-s %s shell wm size" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        results = re.search(r"Physical size:(.*)", results.decode())
        if results:
            results = results.group(1)
        return results

    @eliminate_blank_space
    def get_maximum_memory(self) ->str :
        # 获取最大内存
        cmd = "-s %s shell cat /proc/meminfo" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        results = re.search(r"MemTotal:(.*)", results.decode())
        if results:
            results = results.group(1)
        return results

    @eliminate_blank_space
    def get_number_cpu_cores(self):
        # 获取设备核数
        cmd = "-s %s shell cat /proc/cpuinfo" % (self.device_id)
        results =  self.us_cmd(cmd)
        cpu_core_num = None
        for item in results:
            item = item.decode()
            cpu_core_num = re.search(r"CPU architecture:(.*)", item)
            if cpu_core_num:
                cpu_core_num = cpu_core_num.group(1)
                break

        return cpu_core_num

    @eliminate_special_symbols
    def get_ipaddress(self) ->str :
        # 获取设备ip地址
        cmd = "-s %s shell ifconfig wlan0 | grep 'inet addr'" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        return results.decode()

    def get_current_remaining_memory(self) ->str :
        # 获取设备当前剩余内存
        cmd = "-s %s shell getprop ro.product.model" % (self.device_id)
        results = self.us_cmd(cmd)[0]
        return results.decode()


class IosInfo:
    # todo:实现IOS提取设备信息
    pass


class PhoneInfo:
    __Android_devices = AndroidInfo
    __Ios_devices = IosInfo

    def __init__(self, device_type, device_id):
        self.device_info = {}
        if device_type == 'android':
            self.phone_device = self.__Android_devices(device_id)
            self.device_info['platformName'] = 'Android'
        else:
            self.phone_device = self.__Ios_devices()
            self.device_info['platformName'] = 'IOS'

    def get_device_info(self):
        # todo: 根据type返回设备信息， all返回全部设备信息
        # todo: 根据device判断并从对应的设备平台获取信息
        device_brand = self.phone_device.get_device_brand()
        model_device = self.phone_device.get_model_device()
        device_name = self.phone_device.get_device_name()
        system_version = self.phone_device.get_device_system_version()
        device_resolution = self.phone_device.get_device_resolution()
        maximum_memory = self.phone_device.get_maximum_memory()
        cpu_cores = self.phone_device.get_number_cpu_cores()
        # ipaddress = self.phone_device.get_ipaddress()
        device_info = {
            "device_brand": device_brand,
            "model_device": model_device,
            "device_name": device_name,
            "platformVersion": system_version,
            "device_resolution": device_resolution,
            "maximum_memory": maximum_memory,
            "cpu_cores": cpu_cores,
            # "ipaddress": ipaddress
        }
        return device_info


if __name__ == '__main__':
    phone_info = PhoneInfo('android', '966d5386')
    print(phone_info.get_device_info())