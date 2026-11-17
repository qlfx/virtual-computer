"""运行工作区命令，生成与本脚本同名的 JSON 快照。"""

import json
from pathlib import Path

if __package__:
    from .WorkingSpaceTreeCommands import WorkingSpaceTools
else:
    from WorkingSpaceTreeCommands import WorkingSpaceTools


def main() -> None:
    workspace = WorkingSpaceTools(Path(__file__).stem, overwrite=True)
    workspace.register_function(
        {"bank": "Function_Memory", "offset": 0}, "더", ["left", "right"]
    )

    workspace.create_WorkingSpace()
    workspace.register_variable({"bank": "WorkSpace_Memory", "offset": 0}, "x", "Int")

    workspace.create_WorkingSpace()
    workspace.register_variable({"bank": "WorkSpace_Memory", "offset": 4}, "y", "Int")

    output = workspace.WorkingSpace_File_Path
    text = output.read_text(encoding="utf-8")
    root = json.loads(text)
    assert root["WorkingSpace0"]["function"][0]["name"] == "더"
    assert root["WorkingSpace1"]["variable"][0]["name"] == "x"
    assert root["WorkingSpace2"]["variable"][0]["name"] == "y"
    print(f"JSON 快照：{output}")
    print(text, end="")


if __name__ == "__main__":
    main()
