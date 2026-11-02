# 2. 抽象操作指令

当前里程碑：设计韩语字符命令，通过解释器执行 `.kr` 程序，实现程序文本的自再现（quine）。

## 韩语 quine

```console
python -X utf8 02_abstract_instructions/hankuk/main.py 02_abstract_instructions/hankuk/quine.kr
```

| 文件 | 职责 |
| --- | --- |
| `hankuk/main.py` | 读取 UTF-8 `.kr` 文件并交给解释器 |
| `hankuk/hankuk_quine_interpret.py` | 分词、登记变量、检查引用、执行打印 |
| `hankuk/quine.kr` | 韩语 quine 程序 |

现有语法：

| 写法 | 含义 |
| --- | --- |
| `것:[文本]` | 将括号内部文本绑定到变量 `것`，内部内容作为数据保存 |
| `쓰것` | 输出变量 `것` 的内容 |
| `쓰[`、`쓰]` | 输出左右方括号 |
| 引用区外的空白 | 分隔命令 |

解释器先登记变量与检查引用，再执行输出，因此支持先引用、后定义。`compile` 是现有函数名，其行为是解释执行，并不生成机器码。当前只支持名为 `것` 的变量定义。

`quine.kr` 的完整程序是：

```text
쓰것 쓰[ 쓰것 쓰] 것:[쓰것 쓰[ 쓰것 쓰] 것:]
```

程序输出与源文本相同，源文件无末尾换行。它处理的是 Python 字符串与变量表；将这些操作落到模块 1 的模拟内存是下一阶段工作。

## 其他表示与自指实验

- `quines/quine.py`：Python quine。
- `quines/quine.hs`：Haskell 草稿，包含未定义的 `it`，尚未完成。
- `encoding/file_parse.py`：自定义四位编码与“按文件类型解释内容”的早期实验。
- `encoding/hv_encoding_lab.py`：横竖笔画几何的多种二进制编码实验，使用标准库。
- `encoding/doodle_code_0101.png` 与 `encoding/doodle_processed/`：图形编码、重绘图像与验证记录；图像生成脚本需要 Pillow。

这些编码实验保留为探索资料，并不表示已经定义统一指令集。
