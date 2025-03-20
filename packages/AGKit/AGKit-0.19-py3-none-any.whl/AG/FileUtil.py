from AG.IOUtil import IOUtil


class FileUtil(IOUtil):
    """文件操作工具类，继承自IOUtil类，提供文件创建和写入功能。"""

    @staticmethod
    def create(path, content, mode, encoding="utf8"):
        """创建并写入文本内容到指定路径的文件。

        Args:
            path (str): 文件路径。
            content (str): 需要写入的文本内容。
            mode (str): 文件打开模式（如'w'覆盖写入，'a'追加写入）。
            encoding (str, optional): 字符编码格式，默认使用'utf8'。

        Returns:
            None
        """
        with open(path, mode, encoding=encoding) as file:
            file.write(content)

    @staticmethod
    def create_lines(path, lines, mode, encoding="utf8"):
        """创建并写入多行文本内容到指定路径的文件。

        Args:
            path (str): 文件路径。
            lines (list): 需要写入的文本行列表（每个元素为字符串）。
            mode (str): 文件打开模式（如'w'覆盖写入，'a'追加写入）。
            encoding (str, optional): 字符编码格式，默认使用'utf8'。

        Returns:
            None
        """
        with open(path, mode, encoding=encoding) as file:
            file.writelines(lines)

    @staticmethod
    def create_binary(path, binary, mode):
        """创建并写入二进制数据到指定路径的文件。

        Args:
            path (str): 文件路径。
            binary (bytes): 需要写入的二进制数据。
            mode (str): 文件打开模式（如'wb'二进制写入模式）。

        Returns:
            None
        """
        with open(path, mode) as file:
            file.write(binary)
