import os
from configparser import ConfigParser

from common import PathUtils

from common.Singleton import Singleton


# 读取配置文件
def get(key, section='default', fallback=None):
    cp = ConfigParserHolder().get()
    return cp.get(section, key, fallback=fallback)


@Singleton
class ConfigParserHolder:
    _cp = None

    def __init__(self):
        # 读取配置文件
        config_file = PathUtils.get_work_dir() + '/config.ini'
        if not os.path.isfile(config_file):
            print('配置文件 config.ini 不存在，请将程序根目录的 config_temp.ini 文件拷贝一份并命名为 config.ini。注意要自行调整其中的配置项。')
            exit(1)
        if not os.access(config_file, os.R_OK):
            print('配置文件 config.ini 不可读，请将程序根目录的 config_temp.ini 文件拷贝一份并命名为 config.ini。注意要自行调整其中的配置项。')
            exit(1)

        cp = ConfigParser()
        cp.read(config_file, encoding='utf-8')
        self._cp = cp

    def get(self):
        return self._cp
