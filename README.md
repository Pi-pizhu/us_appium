第一版appium自动化测试框架，需要添加配置文件读取及添加文件锁功能
#### capabilities.json配置文件

文件格式：
- device_id:
    - using_state：是否已被其他进程appium使用 no/yes
    - caps：配置信息
    

caps 配置信息必备参数：
- appPackage：包名
- appActivity：启动activity

可选参数：参照driver_caps里的配置参数