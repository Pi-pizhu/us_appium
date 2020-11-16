import configparser


class MyConfigParser(configparser.ConfigParser):
    """
    解决configparser自动转换字母大小写问题
    """
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr