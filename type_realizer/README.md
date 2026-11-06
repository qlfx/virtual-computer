# 类型布局

[type_realizer.py](type_realizer.py) 使用已经登记的类型定义组合布局。传入非空的成员类型列表和未使用的新名称，即可登记按顺序排列的成员及其总位宽。例如 `[Int, Bool, Bool]` 占 6 位。

位宽与成员顺序用于内存分配。命题的逻辑结构、证明项的类型和依赖字段属于[后续证明检查计划](../docs/proof-checking-roadmap.md)。

[prototype](prototype/) 保留早期韩语音节到位操作的独立实验。
