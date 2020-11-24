#### us_appium自动化测试框架
通过python + appium + allure搭建完成的UI自动化测试框架。

关键点：

- run.py初始化、接收命令，通过pytest.main()进行测试
- 使用pytest-xdist进行多进程并行测试
- 通过fcntl.lock的方式对driver配置文件进行加锁，防止多进程使用设备冲突
- 测试目录下必须有settings.ini文件，设置基础的配置信息
- 初始化文件结构
    - log
        - 当前年月日
            - appium 日志
            - test 测试运行日志
                - *.run.main.log : run.py主进程运行时初始化日志
                - *.run.log : 子进程运行时的日志
                
目录结构：
- BaseAdb：adb命令
- BaseAppiumServer：appium server操作
- BasePhoneInfo：设备信息获取
- driver_base：driver操作二次封装
- file_plugin：文件操作
- make：创建初始化
- mobile_core：driver实例生成、caps配置信息获取解析
- run.py：初始化操作，pytest.main()入口