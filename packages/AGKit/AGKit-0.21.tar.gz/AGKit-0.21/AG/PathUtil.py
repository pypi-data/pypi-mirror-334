import os


class PathUtil:
    @staticmethod
    def GetRoot():
        return os.getcwd()

    @staticmethod
    def AbsPath(path):
        return os.path.abspath(path)
