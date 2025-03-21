from typing import Callable, List, Optional, Any
from io import BytesIO
# from typing import TypeVar

class BinaryReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def read_int(self) -> int:
        result = int.from_bytes(self.data[self.pos:self.pos + 4], "little", signed=True)
        self.pos += 4
        return result

    def read_long(self) -> int:
        result = int.from_bytes(self.data[self.pos:self.pos + 8], "little", signed=True)
        self.pos += 8
        return result

    def read_string(self) -> str:
        length = self.data[self.pos]
        self.pos += 1
        if length == 254:
            length = int.from_bytes(self.data[self.pos:self.pos + 3], "little")
            self.pos += 3
        result = self.data[self.pos:self.pos + length].decode("utf-8")
        self.pos += length
        while self.pos % 4 != 0:
            self.pos += 1
        return result

    def read_bytes(self, length: int) -> bytes:
        result = self.data[self.pos:self.pos + length]
        self.pos += length
        return result