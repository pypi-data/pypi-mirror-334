from typing import Any, Dict, List, Tuple
import struct
from neongram.parser.tl_parser import TLParameter, TLType

class TLObject:
    def serialize(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: bytes, offset: int) -> Tuple["TLObject", int]:
        raise NotImplementedError


class TLConstructor(TLObject):
    def __init__(self, name: str, crc32: int, params: List["TLParameter"], tl_type: "TLType"):
        self.name = name
        self.crc32 = crc32
        self.params = params
        self.type = tl_type
        self.values: Dict[str, Any] = {}

    def serialize(self) -> bytes:
        result = struct.pack("<I", self.crc32)
        flags = self._calculate_flags()

        if any(param.is_flag for param in self.params):
            result += struct.pack("<I", flags)

        for param in self.params:
            if param.name in self.values:
                if param.is_flag:
                    if self.values[param.name]:
                        result += self._serialize_value(param.type, self.values[param.name])
                else:
                    result += self._serialize_value(param.type, self.values[param.name])

        return result

    def _calculate_flags(self) -> int:
        flags = 0
        for param in self.params:
            if param.is_flag and param.name in self.values and self.values[param.name]:
                flags |= 1 << param.flag_bit
        return flags

    def _serialize_value(self, param_type: str, value: Any) -> bytes:
        if param_type == "int":
            return struct.pack("<i", value)
        elif param_type == "long":
            return struct.pack("<q", value)
        elif param_type == "double":
            return struct.pack("<d", value)
        elif param_type == "string":
            return self._serialize_string(value)
        elif param_type == "bytes":
            return self._serialize_bytes(value)
        elif isinstance(value, TLObject):
            return value.serialize()
        elif param_type.startswith("Vector"):
            return self._serialize_vector(param_type, value)
        raise ValueError(f"Unsupported type: {param_type}")

    def _serialize_string(self, value: str) -> bytes:
        encoded = value.encode("utf-8")
        return self._serialize_bytes(encoded)

    def _serialize_bytes(self, value: bytes) -> bytes:
        length = len(value)
        if length <= 253:
            padding = (4 - (length + 1) % 4) % 4
            return struct.pack("B", length) + value + b"\x00" * padding
        padding = (4 - length % 4) % 4
        return b"\xfe" + struct.pack("<I", length)[:3] + value + b"\x00" * padding

    def _serialize_vector(self, param_type: str, values: List[Any]) -> bytes:
        inner_type = param_type.split("<")[1][:-1]
        result = struct.pack("<I", 0x1cb5c415)
        result += struct.pack("<I", len(values))
        for value in values:
            result += self._serialize_value(inner_type, value)
        return result

    @classmethod
    def deserialize(cls, data: bytes, offset: int) -> Tuple["TLObject", int]:
        raise NotImplementedError("Deserialization requires parser instance")


class TLFunction(TLObject):
    def __init__(
        self, name: str, crc32: int, params: List["TLParameter"], return_type: str
    ):
        self.name = name
        self.crc32 = crc32
        self.params = params
        self.return_type = return_type
        self.values: Dict[str, Any] = {}

    def serialize(self) -> bytes:
        result = struct.pack("<I", self.crc32)
        flags = self._calculate_flags()

        if any(param.is_flag for param in self.params):
            result += struct.pack("<I", flags)

        for param in self.params:
            if param.name in self.values:
                if param.is_flag:
                    if self.values[param.name]:
                        result += self._serialize_value(param.type, self.values[param.name])
                else:
                    result += self._serialize_value(param.type, self.values[param.name])

        return result

    def _calculate_flags(self) -> int:
        flags = 0
        for param in self.params:
            if param.is_flag and param.name in self.values and self.values[param.name]:
                flags |= 1 << param.flag_bit
        return flags

    def _serialize_value(self, param_type: str, value: Any) -> bytes:
        if param_type == "int":
            return struct.pack("<i", value)
        elif param_type == "long":
            return struct.pack("<q", value)
        elif param_type == "double":
            return struct.pack("<d", value)
        elif param_type == "string":
            return self._serialize_string(value)
        elif param_type == "bytes":
            return self._serialize_bytes(value)
        elif isinstance(value, TLObject):
            return value.serialize()
        elif param_type.startswith("Vector"):
            return self._serialize_vector(param_type, value)
        raise ValueError(f"Unsupported type: {param_type}")

    def _serialize_string(self, value: str) -> bytes:
        encoded = value.encode("utf-8")
        return self._serialize_bytes(encoded)

    def _serialize_bytes(self, value: bytes) -> bytes:
        length = len(value)
        if length <= 253:
            padding = (4 - (length + 1) % 4) % 4
            return struct.pack("B", length) + value + b"\x00" * padding
        padding = (4 - length % 4) % 4
        return b"\xfe" + struct.pack("<I", length)[:3] + value + b"\x00" * padding

    def _serialize_vector(self, param_type: str, values: List[Any]) -> bytes:
        inner_type = param_type.split("<")[1][:-1]
        result = struct.pack("<I", 0x1cb5c415)
        result += struct.pack("<I", len(values))
        for value in values:
            result += self._serialize_value(inner_type, value)
        return result

    @classmethod
    def deserialize(cls, data: bytes, offset: int) -> Tuple["TLObject", int]:
        raise NotImplementedError("Deserialization requires parser instance")