import os.path
import shutil

from AG import Logger
from AG.IOUtil import IOUtil


class DirUtil(IOUtil):
    @staticmethod
    def Check(path, auto_create=True):
        """
        检查目录路径
        :param path:目录路径
        :param auto_create:不存在是是否自动创建
        :return:目录是否存在
        """
        if DirUtil.Exists(path):
            return True
        else:
            Logger.Instance.Error(f"目录不存在：{path}")
            if auto_create:
                Logger.Instance.Info(f"创建目录：{path}")
                DirUtil.Create(path)
                return True
        return False

    @staticmethod
    def Create(path):
        """
        创建目录
        :param path:目录路径
        :return:-
        """
        if not DirUtil.Exists(path):
            os.makedirs(path)

    @staticmethod
    def Delete(path):
        """
        删除目录
        :param path:目录路径
        :return:-
        """
        if DirUtil.Exists(path):
            Logger.Instance.Info(f"删除目录：{path}")
            shutil.rmtree(path)

    @staticmethod
    def Clear(path):
        """
        清空目录
        :param path:目录路径
        :return:-
        """
        DirUtil.Delete(path)
        DirUtil.Check(path)
