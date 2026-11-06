# Virtual Computer · 形式化验证语言与模拟硬件实验

这是一个从零设计小型形式化验证语言和配套模拟硬件的实验。项目用 Python 搭建原型，研究如何把命题与证明表示成可检查的程序，以及如何把定理应用、变量代换和等式改写落实为类型规则与机器指令。

## 当前进度

| 模块 | 已实现 |
| --- | --- |
| [位内存](memory_simulation/README.md) | 创建指定容量的内存块，以列表保存比特 |
| [读写与分配](memory_for_caculation/README.md) | 按位地址读写，查找单块内存中的连续空间 |
| [类型布局](type_realizer/README.md) | 登记基础类型和组合类型，保存成员顺序与总位宽 |
| [命令原型](programming_language/starter_formal_verifier/commands.py) | 声明变量，登记类型与地址，更新块内剩余容量 |

## 后续实验

先实现最小的证明检查器，验证如何由 `P → Q` 和 `Q → R` 推出 `P → R`。之后用子群判定定理检验群公理的表示、定理实例化和等式改写，并据此探索公式读取、类型比较与代换所需的指令。具体设计和验收样例见[形式化证明检查计划](docs/proof-checking-roadmap.md)。

## 运行当前原型

在仓库根目录使用 PowerShell 运行变量声明演示：

```powershell
$env:PYTHONPATH = (Resolve-Path memory_simulation,memory_for_caculation,type_realizer).Path -join [IO.Path]::PathSeparator
python -B -X utf8 programming_language/starter_formal_verifier/commands.py
```

`PYTHONPATH` 为不同位置的检出目录提供模块搜索路径。演示分配两个 1 位的 `Bool` 和一个 6 位的组合类型。

## 早期实验

[韩语 quine](programs/quine.kr) 由独立解释器输出自身源文本。其他早期实验可在 Git 历史和[迁移记录](docs/file-migration.json)中查找。

```powershell
python -B -X utf8 -m programming_language.hankuk.main programs/quine.kr
```
