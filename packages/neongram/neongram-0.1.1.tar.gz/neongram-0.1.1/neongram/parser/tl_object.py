# src/neongram/mtproto/schema/tl_object.py
from typing import List, Dict, Any
from neongram.utils.binary_writer import BinaryWriter
from neongram.utils.binary_reader import BinaryReader

class TLObject:
    def __init__(self, name: str, constructor_id: int):
        self._ = name
        self.constructor_id = constructor_id

    def to_bytes(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)
        return writer.get_bytes()

    @classmethod
    def from_reader(cls, reader: BinaryReader) -> "TLObject":
        return cls("", 0)

class TLFunction(TLObject):
    def __init__(self, name: str, constructor_id: int, params: List[Dict[str, Any]], return_type: str):
        super().__init__(name, constructor_id)
        self.params = params
        self.return_type = return_type
        self.values: Dict[str, Any] = {}

    def serialize(self) -> bytes:
        writer = BinaryWriter()
        writer.write_int(self.constructor_id)
        for param in self.params:
            name = param["name"]
            value = self.values.get(name)
            if value is not None:
                if param["type"] == "int":
                    writer.write_int(value)
                elif param["type"] == "string":
                    writer.write_string(value)
                elif param["type"] == "int128":
                    writer.write_bytes(value.to_bytes(16, "little"))
                elif isinstance(value, dict) and "_" in value:
                    writer.write_string(value["_"])
        return writer.get_bytes()