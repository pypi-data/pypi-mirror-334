import os.path
import shutil

from AG import Logger
from AG.IOUtil import IOUtil


class DirUtil(IOUtil):
    @staticmethod
    def check(path, auto_create=True):
        """
        检查目录路径
        :param path: 目录路径
        :param auto_create: 不存在时是否自动创建
        :return: 目录是否存在（自动创建后返回True）
        """
        if DirUtil.exists(path):
            return True
        else:
            Logger.ins.error(f"目录不存在：{path}")
            if auto_create:
                Logger.ins.info(f"创建目录：{path}")
                DirUtil.create(path)
                return True
        return False

    @staticmethod
    def create(path):
        """
        创建目录
        :param path: 目录路径
        :return: None
        """
        if not DirUtil.exists(path):
            os.makedirs(path)

    @staticmethod
    def delete(path):
        """
        删除目录
        :param path: 目录路径
        :return: None
        """
        if DirUtil.exists(path):
            Logger.ins.info(f"删除目录：{path}")
            shutil.rmtree(path)

    @staticmethod
    def clear(path):
        """
        清空目录（删除后重新创建）
        :param path: 目录路径
        :return: None
        """
        DirUtil.delete(path)
        DirUtil.check(path)
