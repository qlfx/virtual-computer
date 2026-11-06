# 内存读写与分配

[memory_operator.py](memory_operator.py) 接收 `Memory` 对象，根据位地址与宽度读写其中的比特列表，并提供块内可用空间查询。当前配置包含两块各 8 位的内存。

变量必须完整存放在同一块内存中。[声明命令](../programming_language/starter_formal_verifier/commands.py)遍历现有块，选出可容纳变量的块，再更新容量以及变量名、类型和地址记录。

基础布局为 `Int` 4 位、`Char` 8 位、`Bool` 1 位。当前的位读写接口依赖调用者传入有效地址、宽度和位流。写入校验随上层编码接口开发。
