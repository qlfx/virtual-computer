# Virtual Computer · 虚拟计算机实验

这个项目用 Python 模拟位内存、类型布局和变量分配，逐步探索一台面向形式化证明检查的虚拟机器需要哪些指令。

| 模块 | 当前工作 |
| --- | --- |
| [位内存](memory_simulation/README.md) | 创建指定容量的内存块，以列表保存比特 |
| [读写与分配](memory_for_caculation/README.md) | 按位地址读写，查找单块内存中的连续空间 |
| [类型布局](type_realizer/README.md) | 登记基础类型和组合类型，保存成员顺序与总位宽 |
| [命令原型](programming_language/starter_formal_verifier/commands.py) | 声明变量，登记类型与地址，更新块内剩余容量 |
| [韩语 quine](programs/quine.kr) | 由独立的韩语解释器输出自身源文本 |

在仓库根目录使用 PowerShell 运行变量声明演示：

```powershell
$env:PYTHONPATH = (Resolve-Path memory_simulation,memory_for_caculation,type_realizer).Path -join [IO.Path]::PathSeparator
python -B -X utf8 programming_language/starter_formal_verifier/commands.py
```

`PYTHONPATH` 为不同位置的检出目录提供模块搜索路径。演示分配两个 1 位的 `Bool` 和一个 6 位的组合类型。

运行独立的韩语 quine：

```powershell
python -B -X utf8 -m programming_language.hankuk.main programs/quine.kr
```

韩语解释器目前使用自己的变量环境。早期实验可在 Git 历史和[迁移记录](docs/file-migration.json)中查找。

## 后续工作

[形式化证明检查计划](docs/proof-checking-roadmap.md)记录从命题逻辑到子群判定的设计思路。当前实现覆盖内存、布局和变量声明，证明项检查与群论推导属于后续里程碑。
