import json
from pathlib import Path
class WorkingSpaceTools:
    def __init__(self, file_name, *, overwrite=False):
        self.WorkingSpace_File_Name = file_name + "_working_space.json"
        self.WorkingSpace_File_Path = self.create_file(self.WorkingSpace_File_Name, overwrite=overwrite)
        self.WorkingSpace_Counter = 1
        self.current_WorkingSpace_number = 0

    def create_file(self, file_name, *, overwrite=False):
        folder = Path(__file__).resolve().parent
        json_name = Path(file_name).with_suffix(".json").name
        path = folder / json_name
        with path.open("w" if overwrite else "x", encoding="utf-8") as file:
            json.dump({"WorkingSpace0": {}}, file, ensure_ascii=False, indent=2)
        return path

    def create_WorkingSpace(self):
        with self.WorkingSpace_File_Path.open("r",encoding = "utf-8") as file:
            data = json.load(file)
        workingspace_name = "WorkingSpace" + str(self.WorkingSpace_Counter)
        data.setdefault(workingspace_name, {})
        with self.WorkingSpace_File_Path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        self.WorkingSpace_Counter = self.WorkingSpace_Counter + 1
        self.current_WorkingSpace_number = self.current_WorkingSpace_number + 1

    #     在文件里创建一个叫做workingspacei的空节点,i为工作区的计数,值为self.WorkingSpace_Counter
    #     self.WorkingSpace_Counter = self.WorkingSpace_Counter + 1

    def register_variable(self, address, name, type, *, value=None):
        record = {"address": address, "name": name, "type": type}
        if value is not None:
            record["value"] = value
        self._register("variable", record)

    def register_function(self, address, name, bundings):
        self._register("function", {"address": address, "name": name, "bundings": bundings})

    def _register(self, kind, record):
        workingspace_name = "WorkingSpace" + str(self.current_WorkingSpace_number)
        with self.WorkingSpace_File_Path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        parent = data[workingspace_name]
        records = parent.setdefault(kind, [])
        if isinstance(records, dict):
            # 兼容之前只保存一条记录的格式。
            records = parent[kind] = [records]
        records.append(record)
        text = json.dumps(data, ensure_ascii=False, indent=2)
        self.WorkingSpace_File_Path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    t = WorkingSpaceTools("workspace_demo", overwrite=True)
    t.create_WorkingSpace()
    t.create_WorkingSpace()
    t.register_variable("undefined", "x", "Int")
    t.register_function("undefined", "더", ["left", "right"])
