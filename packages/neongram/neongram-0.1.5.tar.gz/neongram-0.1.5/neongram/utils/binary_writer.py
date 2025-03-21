from typing import Callable, List, Optional, Any
from io import BytesIO


class BinaryWriter:
    def __init__(self):
        self._bytes = bytearray()

    def write_int(self, value: int) -> None:
        self._bytes.extend(value.to_bytes(4, "little", signed=True))

    def write_long(self, value: int) -> None:
        self._bytes.extend(value.to_bytes(8, "little", signed=True))

    def write_string(self, value: str) -> None:
        encoded = value.encode("utf-8")
        length = len(encoded)
        if length <= 253:
            self._bytes.append(length)
        else:
            self._bytes.append(254)
            self._bytes.extend(length.to_bytes(3, "little"))
        self._bytes.extend(encoded)
        while len(self._bytes) % 4 != 0:
            self._bytes.append(0)

    def write_bytes(self, value: bytes) -> None:
        self._bytes.extend(value)

    def get_bytes(self) -> bytes:
        return bytes(self._bytes)