import xlrd

from AG.Logger import Logger


class Excel:
    @staticmethod
    def get_sheets(path):
        """
        获取Excel工作簿中的所有工作表
        :param path: Excel文件路径（字符串类型）
        :return: 工作表列表（若文件无效则返回None）
        """
        if Excel.is_excel_valid(path):
            excel = xlrd.open_workbook(path)
            return excel.sheets()
        return None

    @staticmethod
    def is_excel_valid(path):
        """
        验证Excel文件格式是否为有效的.xls格式
        :param path: 文件路径（字符串类型）
        :return: 布尔值（True表示格式有效，False表示格式无效）
        """
        if path.endswith(".xls"):
            return True
        Logger.ins.error("%s文件格式异常，请确保表格文件为.xls格式" % path)
        return False

    @staticmethod
    def is_sheet_valid(sheet):
        """
        验证工作表是否有效
        :param sheet: 要验证的工作表对象
        :return: 布尔值（若工作表名称以"No"开头则无效返回False，否则有效返回True）
        """
        info = sheet.name.split("_")
        if info[0].lower() == "no":
            return False
        return True

    @staticmethod
    def get_cell_value(sheet, row, col):
        """
        获取工作表中指定单元格的值
        :param sheet: 工作表对象
        :param row: 单元格所在行号（从0开始）
        :param col: 单元格所在列号（从0开始）
        :return: 根据单元格类型返回对应值（空字符串、字符串或数值）
        """
        cell = sheet.cell(row, col)
        c_type = cell.ctype
        c_value = cell.value
        # 处理空单元格（类型0）
        if c_type == 0:
            return ""
        # 处理字符串类型（类型1）
        elif c_type == 1:
            return c_value
        # 处理数值类型（类型2），判断是否为整数
        elif c_type == 2:
            if c_value % 1 == 0.0:
                return int(c_value)
            else:
                return c_value
