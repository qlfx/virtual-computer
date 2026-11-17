"""用可序列化为 JSON 的树记录工作区及其绑定。"""

import json
from copy import deepcopy


class WorkingSpaceTree:
    def __init__(self):
        self.root: dict = {"bindings": [], "children": []}
        self._active_scopes = [self.root]

    @property
    def current(self) -> dict:
        """返回当前作用域。"""
        return self._active_scopes[-1]

    def enter_scope(self, child_index: int | None = None) -> dict:
        """无下标时创建子作用域，否则进入指定的已有子作用域。"""
        children = self.current["children"]
        if child_index is None:
            child = {"bindings": [], "children": []}
            children.append(child)
        else:
            child = children[child_index]
        self._active_scopes.append(child)
        return child

    def exit_scope(self) -> None:
        """返回父作用域，保留刚离开的子树。"""
        if len(self._active_scopes) == 1:
            raise ValueError("根工作区不能退出")
        self._active_scopes.pop()

    def remove_scope(self, child_index: int) -> dict:
        """按下标删除当前作用域的一个直接子树。"""
        return self.current["children"].pop(child_index)

    def add_variable(self, name: str, type_name: str, address) -> None:
        """登记已分配的变量地址和类型。"""
        self._add_binding({
            "kind": "variable", "name": name, "address": address, "type": type_name,
        })

    def add_function(self, name: str, address, bindings: list | None = None) -> None:
        """以名字登记外部函数的地址和绑定序列。"""
        if bindings is not None and not isinstance(bindings, list):
            raise TypeError("函数的 bindings 必须是列表")
        self._add_binding({
            "kind": "function",
            "name": name,
            "address": address,
            "bindings": [] if bindings is None else bindings,
        })

    def _add_binding(self, binding: dict) -> None:
        name = binding["name"]
        if not isinstance(name, str) or not name:
            raise ValueError("绑定名称必须是非空字符串")

        local_bindings = self.current["bindings"]
        if any(existing["name"] == name for existing in local_bindings):
            raise ValueError(f"当前工作区已有绑定：{name}")

        json.dumps(binding, allow_nan=False)
        local_bindings.append(deepcopy(binding))

    def lookup(self, name: str) -> dict:
        """由内向外查找最近的同名绑定。"""
        for scope in reversed(self._active_scopes):
            for binding in scope["bindings"]:
                if binding["name"] == name:
                    return binding
        raise NameError(f"找不到绑定：{name}")

    def remove_binding(self, name: str) -> dict:
        """只删除当前作用域中的绑定。"""
        local_bindings = self.current["bindings"]
        for index, binding in enumerate(local_bindings):
            if binding["name"] == name:
                return local_bindings.pop(index)
        raise NameError(f"当前工作区中找不到绑定：{name}")

    def to_json(self) -> str:
        """导出树的 JSON 快照。"""
        return json.dumps(self.root, ensure_ascii=False, indent=2, allow_nan=False)


if __name__ == "__main__":
    tree = WorkingSpaceTree()
    tree.add_function("더", {"bank": "Function_Memory", "offset": 0})
    tree.enter_scope()
    tree.add_variable("x", "Int", {"bank": "WorkSpace_Memory", "offset": 4})
    print(tree.lookup("더"))
    print(tree.to_json())
