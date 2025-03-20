import os
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TLParameter:
    name: str
    type: str
    is_flag: bool = False
    flag_bit: Optional[int] = None


class TLParser:
    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.types: Dict[str, "TLType"] = {}
        self.constructors: Dict[int, "TLConstructor"] = {}
        self.functions: Dict[str, "TLFunction"] = {}
        self.parse_schema()

    def parse_schema(self) -> None:
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        with open(self.schema_path, "r", encoding="utf-8") as file:
            content = file.read()

        types_section = re.search(r"---types---(.*?)---functions---", content, re.DOTALL)
        functions_section = re.search(r"---functions---(.*)$", content, re.DOTALL)

        if types_section:
            self._parse_types(types_section.group(1))
        if functions_section:
            self._parse_functions(functions_section.group(1))

    def _parse_types(self, content: str) -> None:
        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            match = re.match(r"(\w+)#([0-9a-fA-F]+)\s*(.*?)?\s*=\s*(\w+);", line)
            if match:
                name, crc32, params_str, type_name = match.groups()
                crc32 = int(crc32, 16)
                params = self._parse_params(params_str) if params_str else []

                if type_name not in self.types:
                    self.types[type_name] = TLType(type_name)

                constructor = TLConstructor(name, crc32, params, self.types[type_name])
                self.types[type_name].constructors.append(constructor)
                self.constructors[crc32] = constructor

    def _parse_functions(self, content: str) -> None:
        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            match = re.match(r"(\w+\.\w+)#([0-9a-fA-F]+)\s*(.*?)?\s*=\s*(\w+);", line)
            if match:
                name, crc32, params_str, return_type = match.groups()
                crc32 = int(crc32, 16)
                params = self._parse_params(params_str) if params_str else []
                function = TLFunction(name, crc32, params, return_type)
                self.functions[name] = function

    def _parse_params(self, params_str: str) -> List[TLParameter]:
        params = []
        for param in params_str.split():
            if ":" in param:
                name, type_def = param.split(":", 1)
                flags_match = re.match(r"flags\.(\d+)\?(.+)", type_def)
                if flags_match:
                    flag_bit, param_type = flags_match.groups()
                    params.append(
                        TLParameter(name, param_type, True, int(flag_bit))
                    )
                else:
                    params.append(TLParameter(name, type_def))
        return params

    def get_type(self, type_name: str) -> Optional["TLType"]:
        return self.types.get(type_name)

    def get_constructor(self, crc32: int) -> Optional["TLConstructor"]:
        return self.constructors.get(crc32)

    def get_function(self, function_name: str) -> Optional["TLFunction"]:
        return self.functions.get(function_name)


class TLType:
    def __init__(self, name: str):
        self.name = name
        self.constructors: List["TLConstructor"] = []


class TLConstructor:
    def __init__(
        self, name: str, crc32: int, params: List[TLParameter], tl_type: TLType
    ):
        self.name = name
        self.crc32 = crc32
        self.params = params
        self.type = tl_type


class TLFunction:
    def __init__(
        self, name: str, crc32: int, params: List[TLParameter], return_type: str
    ):
        self.name = name
        self.crc32 = crc32
        self.params = params
        self.return_type = return_type