from neongram.parser.tl_object import TLObject
from neongram.utils.binary_reader import BinaryReader
from neongram.utils.binary_writer import BinaryWriter


class ChatEmpty(TLObject):
    """Represents an empty or deleted chat.

    Args:
        id (int): The chat's unique identifier.
    """

    def __init__(self, id: int):
        super().__init__("chatEmpty", 0x29562865)
        self.id = id

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)
        writer.write_int(self.id)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "ChatEmpty":
        id_ = reader.read_int()
        return cls(id_)