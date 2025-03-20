from AG.Logger import Logger


class LangBase:
    def CreateConst(self, datas, dst):
        Logger.Instance.Info("创建常量文件")
        pass

    def CreateEnum(self, datas, dst):
        Logger.Instance.Info("创建枚举文件")
        pass

    def CreateClass(self, datas, dst):
        Logger.Instance.Info("创建类型文件")
        pass

    def CreateCode(self, head_info, datas, dst):
        Logger.Instance.Info("创建配置代码文件")
        pass

    def CreateCSV(self, head_info, datas, dst):
        Logger.Instance.Info("创建数据文件")
        pass

    def CreateManager(self, class_names, path):
        Logger.Instance.Info("创建管理文件")
        pass

    def CreateUtil(self, path):
        Logger.Instance.Info("创建工具类文件")
        pass

    def GetTypeName(self, type):
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
                Logger.Instance.Error("%s异常字段类型，请检查" % type)
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

    def GetCSVMethodName(self, type):
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
                Logger.Instance.Error("%s异常字段类型，请检查" % type)
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

    def GetBINMethodName(self, type):
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
                Logger.Instance.Error("%s异常字段类型，请检查" % type)
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

    def GetValueWithType(self, type, value):
        lower_type = type.lower()
        if lower_type == "string":
            return "\"%s\"" % value
        return value
