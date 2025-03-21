from typing import List
import os
from neongram.parser.tl_object import TLConstructor, TLType
from neongram.parser.tl_parser import TLParameter 

class TLParser:
    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.constructors = {}
        self.types = {}
        self.parse_schema()

    def parse_schema(self):
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        with open(self.schema_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                if "=" in line:
                    name, rest = line.split("=", 1)
                    crc32_part, rest = rest.split(" ", 1)
                    crc32 = int(crc32_part[1:], 16)  # Extract CRC32 
                    type_name = rest.split(";", 0)[0].strip()
                    params = self._parse_params(rest)
                    self.constructors[name] = TLConstructor(
                        name=name,
                        crc32=crc32,
                        params=params,
                        tl_type=TLType(type_name)
                    )

    def _parse_params(self, param_str: str) -> List[TLParameter]:
        params = []
        param_parts = param_str.split()
        for part in param_parts:
            if ":" in part:
                name, type_name = part.split(":")
                is_flag = type_name.startswith("flags.")  # Simplified flag detection
                flag_bit = int(type_name.split(".")[1].split("?")[0]) if is_flag else None
                param_type = type_name.split("?")[1] if is_flag else type_name
                params.append(
                    TLParameter(
                        name=name,
                        type=param_type,
                        is_flag=is_flag,
                        flag_bit=flag_bit
                    )
                )
        return params
    
class TLParameter:
        def __init__(self, name: str, type: str, is_flag: bool = False, flag_bit: int = None):
          self.name = name
          self.type = type
          self.is_flag = is_flag
          self.flag_bit = flag_bit
          