import configparser

from AG.Logger import Logger
from AG.Singleton import Singleton
from AG.FileUtil import FileUtil


class INI(Singleton):
    """单例模式的INI配置管理类，负责读取和存储INI配置文件。"""
    data = None

    def __init__(self):
        """初始化INI配置管理实例。"""
        self.file_name = ""

    def get_ini(self, section, key):
        """根据指定的节和键获取INI配置值。

        Args:
            section (str): 配置文件中的节名称。
            key (str): 要获取的键名称。

        Returns:
            str or None: 配置键对应的值，若未找到则返回None。
        """
        result = self.data.get(section, key)
        return result

    def init(self, file_name):
        """初始化配置文件路径并加载配置。

        Args:
            file_name (str): 配置文件名（不含扩展名）。

        Returns:
            None
        """
        # 检查配置文件是否存在
        self.file_name = f"{file_name}.ini"
        if not FileUtil.exists(self.file_name):
            Logger.ins.info(f"当前目录下没有找到配置文件：{self.file_name}")
            return

        # 加载配置文件内容
        self.data = configparser.ConfigParser()
        self.data.read(self.file_name, encoding="utf-8")
