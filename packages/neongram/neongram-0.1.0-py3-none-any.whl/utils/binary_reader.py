from typing import Callable, List, Optional, Any
from io import BytesIO
from typing import TypeVar

T = TypeVar('T')


class BinaryReader:
    """A utility class for reading binary data from a byte stream.

    Args:
        data (bytes): The binary data to read from.
    """

    def __init__(self, data: bytes):
        self.stream = BytesIO(data)
        self.length = len(data)

    def read_byte(self) -> int:
        """Reads a single byte as an integer.

        Returns:
            int: The byte value (0-255).
        """
        return self.stream.read(1)[0]

    def read_bytes(self, length: int) -> bytes:
        """Reads a specified number of bytes.

        Args:
            length (int): Number of bytes to read.

        Returns:
            bytes: The read bytes.
        """
        return self.stream.read(length)

    def read_int(self, signed: bool = True) -> int:
        """Reads a 32-bit integer.

        Args:
            signed (bool): Whether the integer is signed.

        Returns:
            int: The integer value.
        """
        value = int.from_bytes(self.stream.read(4), byteorder="little", signed=signed)
        return value

    def read_long(self, signed: bool = True) -> int:
        """Reads a 64-bit integer.

        Args:
            signed (bool): Whether the integer is signed.

        Returns:
            int: The long value.
        """
        value = int.from_bytes(self.stream.read(8), byteorder="little", signed=signed)
        return value

    def read_int128(self) -> int:
        """Reads a 128-bit integer.

        Returns:
            int: The 128-bit integer value.
        """
        value = int.from_bytes(self.stream.read(16), byteorder="little", signed=True)
        return value

    def read_double(self) -> float:
        """Reads a 64-bit double-precision float.

        Returns:
            float: The double value.
        """
        import struct
        return struct.unpack("<d", self.stream.read(8))[0]

    def read_string(self) -> str:
        """Reads a string with length prefix.

        Returns:
            str: The decoded string.
        """
        length = self.read_byte()
        if length == 254:
            length = int.from_bytes(self.stream.read(3), byteorder="little")
        padding = (4 - (length % 4)) % 4
        data = self.stream.read(length)
        self.stream.read(padding)
        return data.decode("utf-8")

    def read_bool(self) -> bool:
        """Reads a boolean value.

        Returns:
            bool: The boolean value.
        """
        value = self.read_int()
        if value == 0x997275b5:
            return True
        if value == 0xbc799737:
            return False
        raise ValueError(f"Invalid boolean value: {value}")

    def read_vector(self, reader_func: Callable[["BinaryReader"], T]) -> List[T]:
        """Reads a vector of elements using a specified reader function.

        Args:
            reader_func (Callable[[BinaryReader], T]): Function to read each element.

        Returns:
            List[T]: List of read elements.
        """
        constructor_id = self.read_int(signed=False)
        if constructor_id != 0x1cb5c415:
            raise ValueError(f"Invalid vector constructor: {constructor_id}")
        count = self.read_int()
        return [reader_func(self) for _ in range(count)]

    def read_obj(self) -> Optional[Any]:
        """Reads a generic object based on its constructor ID.

        Returns:
            Optional[Any]: The deserialized object or None.
        """
        from neongram.parser.tl_object import TLObject
        constructor_id = self.read_int(signed=False)
        if constructor_id == 0:
            return None
        return TLObject.from_reader(self, constructor_id)

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

    def remaining(self) -> int:
        """Gets the number of remaining bytes in the stream.

        Returns:
            int: Number of remaining bytes.
        """
        return self.length - self.stream.tell()