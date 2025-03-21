from neongram.parser.tl_object import TLObject
from neongram.utils.binary_reader import BinaryReader
from neongram.utils.binary_writer import BinaryWriter


class InputChannel(TLObject):
    """Represents a channel for input (used in API requests).

    Args:
        channel_id (int): The channel's identifier.
        access_hash (int): Access hash for the channel.
    """

    def __init__(self, channel_id: int, access_hash: int):
        super().__init__("inputChannel", 0xafeb712e)
        self.channel_id = channel_id
        self.access_hash = access_hash

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)
        writer.write_long(self.channel_id)
        writer.write_long(self.access_hash)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "InputChannel":
        channel_id = reader.read_long()
        access_hash = reader.read_long()
        return cls(channel_id, access_hash)