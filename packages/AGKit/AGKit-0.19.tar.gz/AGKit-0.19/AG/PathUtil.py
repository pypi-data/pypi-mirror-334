import os


class PathUtil:
    """
    提供路径处理实用方法的工具类
    """

    @staticmethod
    def get_root():
        """
        获取当前工作目录的路径。

        参数:
        无

        返回:
        str: 当前工作目录的绝对路径。
        """
        return os.getcwd()

    @staticmethod
    def abs_path(path):
        """
        将给定路径转换为绝对路径。

        参数:
        path (str): 需要转换为绝对路径的输入路径，可以是相对或绝对路径。

        返回:
        str: 输入路径对应的绝对路径。
        """
        return os.path.abspath(path)
