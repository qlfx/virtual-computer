# Virtual Computer · 虚拟计算机实验

通过三个模块研究一台计算机如何从“保存比特”走向“解释并执行程序”：模拟内存、抽象操作指令，以及操作指令到模拟内存的连接。

## 项目层次与进度

| 模块 | 研究的问题 | 当前进度 | 入口 |
| --- | --- | --- | --- |
| 1. 模拟内存 | 位、地址、类型和访问检查怎样组织？ | 已完成第一轮小型内存模拟，另有分页与 mmap 实验 | [01_memory_simulation](01_memory_simulation/README.md) |
| 2. 抽象操作指令 | 字符怎样表示命令，代码怎样成为数据？ | 已通过韩语字符指令实现 quine 自再现 | [02_abstract_instructions](02_abstract_instructions/README.md) |
| 3. 操作指令到模拟内存的连接 | 抽象指令怎样引起内存状态变化？ | 下一阶段；保留初步字符到读写操作的原型 | [03_instruction_memory_bridge](03_instruction_memory_bridge/README.md) |

```mermaid
flowchart LR
    P[韩语程序与字符表示] --> I[模块 2：解析与抽象指令]
    I --> B[模块 3：指令执行与内存接口\n下一阶段]
    B --> M[模块 1：模拟内存]
    M --> S[位、地址与状态变化]
```

上图表达项目要建立的完整执行路径。目前韩语 quine 由 Python 字符串与变量表实现，尚未经过模块 1 的位内存；第三模块的原型也尚未与 quine 解释器形成统一执行路径。

## 运行现有成果

在仓库根目录使用 Python 3.12 或更新版本运行以下命令。主要演示使用标准库。

```console
python -X utf8 01_memory_simulation/virtual_memory_experiment.py
python -X utf8 02_abstract_instructions/hankuk/main.py 02_abstract_instructions/hankuk/quine.kr
python -X utf8 03_instruction_memory_bridge/prototype/memory_wr.py
```

第一条演示文件偏移、进程虚拟地址、模拟页框、共享与缺页。第二条输出 `.kr` 文件的程序文本，解释器不添加换行；样例源文件末尾也没有换行。第三条展示已有的指针移动与位写入原型。

原始 `01_memory_simulation/virtual_machine.py` 会先输出 `203`、`203`、`52171`，随后故意使用未定义类型并抛出 `ValueError`。这是第一轮实验的现有结尾。Haskell quine 仍是草稿，不能作为完整程序运行。

## 文件与实验记录

- [内存模块说明](01_memory_simulation/README.md)：原始位内存、分页模型与实际 mmap 实验。
- [指令模块说明](02_abstract_instructions/README.md)：韩语语法、quine 与其他编码实验。
- [连接模块计划](03_instruction_memory_bridge/README.md)：已有原型、边界和下一阶段路线。
- [历史草稿与备份](archive/README.md)：原目录中的备份与编辑器临时片段。
- [文件迁移记录](docs/file-migration.json)：原路径、新路径与 SHA-256。此次整理保留了 24 个原文件的内容。

图像编码演示中的 `encoding/doodle_processed/generate_demo.py` 另外需要 Pillow；现成 PNG、SVG 和验证记录已经保留。Python 缓存不纳入版本控制。
