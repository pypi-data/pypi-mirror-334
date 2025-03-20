import os


class IOUtil:
    """提供文件和目录操作的工具类。"""

    @staticmethod
    def exists(path):
        """检查指定路径是否存在。

        Args:
            path (str): 需要检查的文件或目录路径。

        Returns:
            bool: 如果路径存在则返回True，否则返回False。
        """
        return os.path.exists(path)
