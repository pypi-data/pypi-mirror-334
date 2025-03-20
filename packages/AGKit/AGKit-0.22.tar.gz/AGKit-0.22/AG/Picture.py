from PIL import Image

from AG import Logger
from AG.FileUtil import FileUtil

# 设置较大的限制值，如None表示无限制，或根据需求设置为具体的大数值
Image.MAX_IMAGE_PIXELS = None


class Picture:
    @staticmethod
    def Open(file_path):
        if not FileUtil.Exists(file_path):
            Logger.Instance.Error("文件不存在：" + file_path)
            return None
        return Image.open(file_path)
