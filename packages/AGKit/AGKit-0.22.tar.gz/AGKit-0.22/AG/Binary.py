import struct


class Binary:
    @staticmethod
    def Write(field_value, field_type):
        if field_type == "int":
            value = Binary.Validate(field_value, int, 0)
            return struct.pack("i", value)
        elif field_type == "short":
            value = Binary.Validate(field_value, int, 0)
            return struct.pack("h", value)
        elif field_type == "byte":
            value = Binary.Validate(field_value, int, 0)
            return struct.pack("b", value)
        elif field_type == "long":
            value = Binary.Validate(field_value, int, 0)
            return struct.pack("q", value)
        elif field_type == "double":
            value = Binary.Validate(field_value, float, 0.0)
            return struct.pack("d", value)
        elif field_type == "bool":
            value = Binary.Validate(field_value, bool, False)
            return struct.pack("?", value)
        else:
            # 找不到的类型先默认为字符串处理
            value = Binary.Validate(field_value, str, "")
            encoded_string = value.encode('utf-8')  # 使用UTF-8编码将字符串转换为字节串
            str_len = len(encoded_string)
            temp_bin = struct.pack("<I", str_len)
            temp_bin += encoded_string
            return temp_bin

    @staticmethod
    def Validate(value, expected_type, default_value):
        """验证数据类型并尝试转换，失败则返回默认值"""
        try:
            if isinstance(value, expected_type):
                return value  # 正确类型，直接返回
            elif expected_type == int:
                return int(value)  # 尝试转换为int
            elif expected_type == float:
                return float(value)  # 尝试转换为float
            elif expected_type == bool:
                return bool(value)  # 尝试转换为bool
            elif expected_type == str:
                return str(value)  # 尝试转换为str
            elif expected_type == bytes:
                return bytes(value)  # 尝试转换为bytes
            else:
                return default_value  # 不支持的类型，返回默认值
        except (ValueError, TypeError):
            return default_value  # 转换失败，返回默认值
