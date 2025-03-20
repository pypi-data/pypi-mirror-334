from AG.Logger import Logger


class LangBase:
    """
    语言基础类，提供创建不同类型配置文件及类型转换的功能

    Attributes:
        None
    """

    def create_const(self, datas: dict, dst: str) -> None:
        """创建常量配置文件

        Args:
            datas (dict): 配置数据字典
            dst (str): 生成的目标文件路径

        Returns:
            None
        """
        Logger.ins.info("创建常量文件")
        pass

    def create_enum(self, datas: dict, dst: str) -> None:
        """创建枚举类型文件

        Args:
            datas (dict): 枚举数据字典
            dst (str): 生成的目标文件路径

        Returns:
            None
        """
        Logger.ins.info("创建枚举文件")
        pass

    def create_class(self, datas: dict, dst: str) -> None:
        """创建数据类型定义文件

        Args:
            datas (dict): 类型定义数据
            dst (str): 生成的目标文件路径

        Returns:
            None
        """
        Logger.ins.info("创建类型文件")
        pass

    def create_code(self, head_info: str, datas: dict, dst: str) -> None:
        """生成配置代码文件

        Args:
            head_info (str): 文件头信息
            datas (dict): 配置数据字典
            dst (str): 生成的目标文件路径

        Returns:
            None
        """
        Logger.ins.info("创建配置代码文件")
        pass

    def create_csv(self, head_info: str, datas: dict, dst: str) -> None:
        """生成CSV数据文件

        Args:
            head_info (str): 文件头信息
            datas (dict): 数据字典
            dst (str): 生成的目标文件路径

        Returns:
            None
        """
        Logger.ins.info("创建数据文件")
        pass

    def create_manager(self, class_names: list, path: str) -> None:
        """创建数据管理类文件

        Args:
            class_names (list): 需要管理的类名列表
            path (str): 生成的文件路径

        Returns:
            None
        """
        Logger.ins.info("创建管理文件")
        pass

    def create_util(self, path: str) -> None:
        """创建工具类文件

        Args:
            path (str): 生成的工具类文件路径

        Returns:
            None
        """
        Logger.ins.info("创建工具类文件")
        pass

    def get_type_name(self, type: str) -> str:
        """根据类型字符串获取对应的类型名称

        Args:
            type (str): 原始类型描述字符串

        Returns:
            str: 处理后的类型名称
        """
        lower_type = type.lower()
        if lower_type == "long":
            return "long"
        elif lower_type == "string":
            return "string"
        elif lower_type == "int":
            return "int"
        elif lower_type == "bool":
            return "bool"
        elif lower_type == "float":
            return "float"
        elif lower_type == "double":
            return "double"
        else:
            sub_types = type.split(":")
            sub_types_len = len(sub_types)
            if sub_types_len == 0:
                Logger.ins.error("%s异常字段类型，请检查" % type)
            elif sub_types_len == 1:
                return type
            elif sub_types_len == 2:
                t_item = sub_types[0]
                c_item = sub_types[1]
                t_item_lower = t_item.lower()
                if t_item_lower == "list":
                    return "List<%s>" % c_item
                if t_item_lower == "enum":
                    return c_item
                else:
                    return c_item + t_item
            elif sub_types_len == 3:
                t_item = sub_types[0]
                k_item = sub_types[1]
                v_item = sub_types[2]
                t_item_lower = t_item.lower()
                if t_item_lower == "dict":
                    return "Dictionary<%s, %s>" % (k_item, v_item)
                else:
                    return type
            else:
                return type

    def get_csv_method_name(self, type: str) -> str:
        """根据类型生成CSV解析方法名称

        Args:
            type (str): 字段类型描述

        Returns:
            str: 对应的CSV解析方法名称
        """
        lower_type = type.lower()
        if lower_type == "long":
            return "Long"
        elif lower_type == "string":
            return "String"
        elif lower_type == "int":
            return "Int"
        elif lower_type == "bool":
            return "Bool"
        elif lower_type == "float":
            return "Float"
        elif lower_type == "double":
            return "Double"
        else:
            sub_types = type.split(":")
            sub_types_len = len(sub_types)
            if sub_types_len == 0:
                Logger.ins.error("%s异常字段类型，请检查" % type)
            elif sub_types_len == 1:
                return type
            elif sub_types_len == 2:
                t_item = sub_types[0]
                c_item = sub_types[1]
                t_item_lower = t_item.lower()
                if t_item_lower == "list":
                    return "%sList" % (c_item[0].upper() + c_item[1:])
                elif t_item_lower == "enum":
                    return "Enum<%s>" % c_item
                else:
                    return c_item
            elif sub_types_len == 3:
                t_item = sub_types[0]
                k_item = sub_types[1]
                v_item = sub_types[2]
                t_item_lower = t_item.lower()
                if t_item_lower == "dict":
                    return "%sDict" % v_item
                else:
                    return type
            else:
                return type

    def get_bin_method_name(self, type: str) -> str:
        """根据类型生成二进制序列化方法名称

        Args:
            type (str): 字段类型描述

        Returns:
            str: 对应的二进制序列化方法名称
        """
        lower_type = type.lower()
        if lower_type == "long":
            return "Long"
        elif lower_type == "string":
            return "String"
        elif lower_type == "int":
            return "Int"
        elif lower_type == "bool":
            return "Bool"
        elif lower_type == "float":
            return "Float"
        elif lower_type == "double":
            return "Double"
        else:
            sub_types = type.split(":")
            sub_types_len = len(sub_types)
            if sub_types_len == 0:
                Logger.ins.error("%s异常字段类型，请检查" % type)
            elif sub_types_len == 1:
                return type
            elif sub_types_len == 2:
                t_item = sub_types[0]
                c_item = sub_types[1]
                t_item_lower = t_item.lower()
                if t_item_lower == "list":
                    return "%sList" % (c_item[0].upper() + c_item[1:])
                elif t_item_lower == "enum":
                    return "Enum<%s>" % c_item
                else:
                    return c_item
            elif sub_types_len == 3:
                t_item = sub_types[0]
                k_item = sub_types[1]
                v_item = sub_types[2]
                t_item_lower = t_item.lower()
                if t_item_lower == "dict":
                    return "%sDict" % v_item
                else:
                    return type
            else:
                return type

    def get_value_with_type(self, type: str, value: str) -> str:
        """根据类型格式化值字符串

        Args:
            type (str): 字段类型描述
            value (str): 原始值字符串

        Returns:
            str: 格式化后的值字符串
        """
        lower_type = type.lower()
        if lower_type == "string":
            return "\"%s\"" % value
        return value
