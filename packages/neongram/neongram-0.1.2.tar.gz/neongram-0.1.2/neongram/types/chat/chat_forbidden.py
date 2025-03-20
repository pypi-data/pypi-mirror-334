from typing import Optional
from neongram.parser.tl_object import TLObject
from neongram.utils.binary_reader import BinaryReader
from neongram.utils.binary_writer import BinaryWriter


class ChatForbidden(TLObject):
    """Represents a chat that the user cannot access.

    Args:
        id (int): The chat's unique identifier.
        title (str): The chat's title.
        date (int, optional): Creation date as Unix timestamp.
    """

    def __init__(self, id: int, title: str, date: Optional[int] = None):
        super().__init__("chatForbidden", 0x6592a1a7)
        self.id = id
        self.title = title
        self.date = date

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)
        writer.write_int(self.id)
        writer.write_string(self.title)
        writer.write_int(self.date if self.date is not None else 0)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "ChatForbidden":
        id_ = reader.read_int()
        title = reader.read_string()
        date = reader.read_int()
        return cls(id_, title, date)