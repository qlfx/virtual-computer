import json
import re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "working_space"))
import WorkingSpaceTreeCommands as wsts
functionlist = []
class Theorem_Interpreter:
    def __init__(self) -> None:
        self.Function_Memory_path = (
    Path(__file__).resolve().parents[1]
    / "working_space"
    / "Function_Memory.json"
    )
        self.function_number = 0
        self.Function_Memory_path.write_text("{}\n", encoding="utf-8")

    def parse_function(self,codes):
        name = []
        typelist = []
        name_pointer = 0
        while codes[name_pointer] != ' ':
            name.append(codes[name_pointer])
            name_pointer = name_pointer + 1
        name_string = "".join(name)

        for i in range(len(codes)):

            if codes[i] == "전":
                type = []
                j = i + 1
                while codes[j] != ',':
                    j = j + 1
                k = j + 1
                while codes[k] != ')':
                   type.append(codes[k])
                   k = k + 1
                type_string = "".join(type)
                typelist.append(type_string)
        with self.Function_Memory_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        function_id = f"function{len(data)}"
        data[function_id] = {
            "name":name_string,
            "parameter_types":typelist,
        }

        text = json.dumps(data, ensure_ascii=False, indent=2)
        self.Function_Memory_path.write_text(text, encoding="utf-8")
        functionlist.append(name_string)
        functionlist.append(typelist)

class Proof_Verifier:
    def __init__(self, file_name="commutative") -> None:
        self.file_name = file_name
        self.workingspace_tool = None

    @staticmethod
    def _parse_declarations(declarations):
        variables = []
        for statement in declarations.split(":"):
            declaration, name = statement.split(")", 1)
            _, fields = declaration.split("(", 1)
            value, type_name = fields.split(",", 1)
            variables.append((name.strip(), type_name.strip(), value.strip()))
        return variables

    @staticmethod
    def _parse_calls(calls):
        functions = []
        for statement in calls.split(":"):
            name, arguments = statement.split("(", 1)
            arguments, _ = arguments.rsplit(")", 1)
            arguments = arguments.strip()
            bindings = [argument.strip() for argument in arguments.split(",")] if arguments else []
            functions.append((name.strip(), bindings))
        return functions

    def parse_proof(self, codes) -> Path:
        text = "".join(codes).strip().strip('“”"').strip()
        declarations, calls = re.split(r"\s+with\s+", text, maxsplit=1)
        variables = self._parse_declarations(declarations)
        functions = self._parse_calls(calls)

        workspace = wsts.WorkingSpaceTools(self.file_name, overwrite=True)
        for name, type_name, value in variables:
            workspace.register_variable("undefined", name, type_name, value=value)
        for name, bindings in functions:
            workspace.register_function("undefined", name, bindings)
        self.workingspace_tool = workspace
        return workspace.WorkingSpace_File_Path

if __name__ == "__main__":
    c = "commutative = “전(x,Z):전(y,Z):는(더(x,y),더(y,x))”"
    p = "“말(2,Z)x:말(3,Z)y:말(5,Z)z with commutative(x,y)”"
    t = Theorem_Interpreter()
    t.parse_function(list(c))
    print(Proof_Verifier().parse_proof(p))
