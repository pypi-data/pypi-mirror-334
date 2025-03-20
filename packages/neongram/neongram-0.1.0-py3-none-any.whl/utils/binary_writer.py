from typing import Callable, List, Optional, Any
from io import BytesIO


class BinaryWriter:
    """A utility class for writing binary data to a byte stream."""

    def __init__(self):
        self.stream = BytesIO()

    def write_byte(self, value: int) -> None:
        """Writes a single byte.

        Args:
            value (int): The byte value (0-255).
        """
        self.stream.write(bytes([value]))

    def write_bytes(self, data: bytes) -> None:
        """Writes a sequence of bytes.

        Args:
            data (bytes): The bytes to write.
        """
        self.stream.write(data)

    def write_int(self, value: int, signed: bool = True) -> None:
        """Writes a 32-bit integer.

        Args:
            value (int): The integer value.
            signed (bool): Whether the integer is signed.
        """
        self.stream.write(value.to_bytes(4, byteorder="little", signed=signed))

    def write_long(self, value: int, signed: bool = True) -> None:
        """Writes a 64-bit integer.

        Args:
            value (int): The long value.
            signed (bool): Whether the integer is signed.
        """
        self.stream.write(value.to_bytes(8, byteorder="little", signed=signed))

    def write_int128(self, value: int) -> None:
        """Writes a 128-bit integer.

        Args:
            value (int): The 128-bit integer value.
        """
        self.stream.write(value.to_bytes(16, byteorder="little", signed=True))

    def write_double(self, value: float) -> None:
        """Writes a 64-bit double-precision float.

        Args:
            value (float): The double value.
        """
        import struct
        self.stream.write(struct.pack("<d", value))

    def write_string(self, value: str) -> None:
        """Writes a string with length prefix.

        Args:
            value (str): The string to write.
        """
        data = value.encode("utf-8")
        length = len(data)
        if length < 254:
            self.write_byte(length)
        else:
            self.write_byte(254)
            self.stream.write(length.to_bytes(3, byteorder="little"))
        self.stream.write(data)
        padding = (4 - (length % 4)) % 4
        if padding:
            self.stream.write(b"\x00" * padding)

    def write_bool(self, value: bool) -> None:
        """Writes a boolean value.

        Args:
            value (bool): The boolean value.
        """
        if value:
            self.write_int(0x997275b5, signed=False)  # true
        else:
            self.write_int(0xbc799737, signed=False)  # false

    def write_vector(self, items: List[Any], writer_func: Callable[["BinaryWriter", Any], None]) -> None:
        """Writes a vector of elements using a specified writer function.

        Args:
            items (List[Any]): List of items to write.
            writer_func (Callable[[BinaryWriter, Any], None]): Function to write each element.
        """
        self.write_int(0x1cb5c415, signed=False)  # Vector constructor
        self.write_int(len(items))
        for item in items:
            writer_func(self, item)

    def write_obj(self, obj: Optional[Any]) -> None:
        """Writes a generic object.

        Args:
            obj (Optional[Any]): The object to write.
        """
        if obj is None:
            self.write_int(0, signed=False)
        else:
            self.stream.write(obj.to_bytes())

    def get_bytes(self) -> bytes:
        """Gets the written bytes.

        Returns:
            bytes: The binary data.
        """
        return self.stream.getvalue()

    def tell(self) -> int:
        """Gets the current position in the stream.

        Returns:
            int: The current position.
        """
        return self.stream.tell()

    def seek(self, position: int) -> None:
        """Seeks to a specific position in the stream.

        Args:
            position (int): Position to seek to.
        """
        self.stream.seek(position)