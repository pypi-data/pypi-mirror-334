from PIL import Image

# 禁用PIL对图像像素数的限制，允许处理超大尺寸的图片
Image.MAX_IMAGE_PIXELS = None


class Picture:
    """提供与图片操作相关的静态方法的工具类。"""

    @staticmethod
    def open(file_path: str) -> Image.Image:
        """打开指定路径的图片文件。

        Args:
            file_path (str): 需要打开的图片文件的绝对或相对路径

        Returns:
            Image.Image: 使用PIL库打开的图片对象
        """
        return Image.open(file_path)
