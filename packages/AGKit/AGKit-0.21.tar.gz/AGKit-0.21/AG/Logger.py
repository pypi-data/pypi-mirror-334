import logging
import colorlog

from AG.Singleton import Singleton


class Logger(Singleton):
    # 日志颜色
    logColors = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    # 输出格式
    format = colorlog.ColoredFormatter(
        # 设置日志格式
        fmt='%(log_color)s[%(levelname)s] %(asctime)s.%(msecs)03d %(message)s',
        # 设置时间格式
        datefmt='%Y-%m-%d %H:%M:%S',
        # 设置日志颜色
        log_colors=logColors
    )
    logger = None
    enable = True

    def __init__(self):
        self.logger = logging.getLogger("QL")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(self.format)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        handler.close()

    def SetEnable(self, enable):
        self.enable = bool(int(enable))

    def Print(self, msg):
        print(msg)

    def Info(self, msg):
        """
        普通打印
        """
        if not self.enable:
            pass
        else:
            self.logger.info(msg)

    def Warn(self, msg):
        """
        警告打印
        """
        if not self.enable:
            pass
        else:
            self.logger.warning(msg)

    def Error(self, msg):
        """
        错误打印
        """
        if not self.enable:
            pass
        else:
            self.logger.error(msg)
