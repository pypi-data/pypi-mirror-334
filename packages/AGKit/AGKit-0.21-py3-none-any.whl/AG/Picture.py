from PIL import Image

# 设置较大的限制值，如None表示无限制，或根据需求设置为具体的大数值
Image.MAX_IMAGE_PIXELS = None


class Picture:
    @staticmethod
    def Open(file_path):
        return Image.open(file_path)
