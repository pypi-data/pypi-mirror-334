from AG.IOUtil import IOUtil


class FileUtil(IOUtil):

    @staticmethod
    def Create(path, content, mode, encoding="utf8"):
        with open(path, mode, encoding=encoding) as file:
            file.write(content)

    @staticmethod
    def CreateLines(path, lines, mode, encoding="utf8"):
        with open(path, mode, encoding=encoding) as file:
            file.writelines(lines)

    @staticmethod
    def CreateBinary(path, binary, mode):
        with open(path, mode) as file:
            file.write(binary)
