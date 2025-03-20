import os


class IOUtil:

    @staticmethod
    def Exists(path):
        return os.path.exists(path)
