from typing import Dict, List
from neongram.parser.tl_parser import TLParser, TLParameter, TLType, TLConstructor, TLFunction
import os


class TLGenerator:
    def __init__(self, parser: TLParser, output_dir: str):
        self.parser = parser
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self) -> None:
        self._generate_types()
        self._generate_methods()

    def _generate_types(self) -> None:
        with open(os.path.join(self.output_dir, "types.py"), "w", encoding="utf-8") as f:
            f.write("neongram.parser.tl_object import TLObject\n")
            f.write("from typing import Dict, Any, List\n\n")

            for tl_type in self.parser.types.values():
                for constructor in tl_type.constructors:
                    class_name = self._to_pascal_case(constructor.name)
                    f.write(f"class {class_name}(TLObject):\n")
                    f.write(f"    crc32 = 0x{constructor.crc32:08x}\n")
                    f.write(f"    tl_type = '{tl_type.name}'\n\n")
                    f.write("    def __init__(self):\n")
                    f.write("        self.values: Dict[str, Any] = {}\n\n")
                    self._write_params(f, constructor.params)
                    f.write("\n")

    def _generate_methods(self) -> None:
        with open(os.path.join(self.output_dir, "methods.py"), "w", encoding="utf-8") as f:
            f.write("from neongram.parser.tl_object import TLFunction\n")
            f.write("from typing import Dict, Any, List\n\n")

            for function in self.parser.functions.values():
                class_name = self._to_pascal_case(function.name.split(".", 1)[1])
                f.write(f"class {class_name}(TLFunction):\n")
                f.write(f"    crc32 = 0x{function.crc32:08x}\n")
                f.write(f"    tl_type = '{function.return_type}'\n")
                f.write(f"    name = '{function.name}'\n\n")
                f.write("    def __init__(self):\n")
                f.write("        self.values: Dict[str, Any] = {}\n\n")
                self._write_params(f, function.params)
                f.write("\n")

    def _write_params(self, file, params: List[TLParameter]) -> None:
        for param in params:
            param_type = self._map_type(param.type)
            prop_name = param.name
            if param.is_flag:
                file.write(f"    @property\n")
                file.write(f"    def {prop_name}(self) -> {param_type}:\n")
                file.write(f"        return self.values.get('{prop_name}')\n\n")
                file.write(f"    @{prop_name}.setter\n")
                file.write(f"    def {prop_name}(self, value: {param_type}) -> None:\n")
                file.write(f"        self.values['{prop_name}'] = value\n\n")
            else:
                file.write(f"    @property\n")
                file.write(f"    def {prop_name}(self) -> {param_type}:\n")
                file.write(f"        return self.values.get('{prop_name}')\n\n")
                file.write(f"    @{prop_name}.setter\n")
                file.write(f"    def {prop_name}(self, value: {param_type}) -> None:\n")
                file.write(f"        self.values['{prop_name}'] = value\n\n")

    def _to_pascal_case(self, name: str) -> str:
        return "".join(word.capitalize() for word in name.split("_"))

    def _map_type(self, tl_type: str) -> str:
        type_map = {
            "int": "int",
            "long": "int",
            "double": "float",
            "string": "str",
            "bytes": "bytes",
            "Bool": "bool",
        }
        if tl_type in type_map:
            return type_map[tl_type]
        if tl_type.startswith("Vector"):
            inner_type = tl_type.split("<")[1][:-1]
            return f"List[{self._map_type(inner_type)}]"
        return tl_type  