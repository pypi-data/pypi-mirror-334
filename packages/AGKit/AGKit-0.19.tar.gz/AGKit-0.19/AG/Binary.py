import struct


class Binary:
    @staticmethod
    def write(field_value, field_type):
        """将给定值根据指定类型转换为二进制格式。
        Args:
            field_value (any): 需要转换的原始数据值。
            field_type (str): 目标类型，支持'int', 'short', 'byte', 'long', 'double', 'bool'或字符串类型。
        Returns:
            bytes: 转换后的二进制数据。若类型不支持，则按字符串处理，返回UTF-8编码的字节串及长度前缀。
        """
        if field_type == "int":
            value = Binary.validate(field_value, int, 0)
            return struct.pack("i", value)
        elif field_type == "short":
            value = Binary.validate(field_value, int, 0)
            return struct.pack("h", value)
        elif field_type == "byte":
            value = Binary.validate(field_value, int, 0)
            return struct.pack("b", value)
        elif field_type == "long":
            value = Binary.validate(field_value, int, 0)
            return struct.pack("q", value)
        elif field_type == "double":
            value = Binary.validate(field_value, float, 0.0)
            return struct.pack("d", value)
        elif field_type == "bool":
            value = Binary.validate(field_value, bool, False)
            return struct.pack("?", value)
        else:
            # 未找到的类型按字符串处理，编码为UTF-8并添加长度前缀
            value = Binary.validate(field_value, str, "")
            encoded_string = value.encode('utf-8')
            str_len = len(encoded_string)
            temp_bin = struct.pack("<I", str_len)
            temp_bin += encoded_string
            return temp_bin

    @staticmethod
    def validate(value, expected_type, default_value):
        """验证数据类型并尝试转换，失败则返回默认值。
        Args:
            value (any): 需要验证的原始值。
            expected_type (type): 期望的目标类型（如int, float, bool等）。
            default_value (any): 类型转换失败时返回的默认值。
        Returns:
            any: 转换后的正确类型值，或转换失败时的默认值。
        """
        try:
            if isinstance(value, expected_type):
                return value
            elif expected_type == int:
                return int(value)
            elif expected_type == float:
                return float(value)
            elif expected_type == bool:
                return bool(value)
            elif expected_type == str:
                return str(value)
            elif expected_type == bytes:
                return bytes(value)
            else:
                return default_value
        except (ValueError, TypeError):
            return default_value
