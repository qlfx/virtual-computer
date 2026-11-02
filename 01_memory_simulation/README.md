# 1. 模拟内存

当前里程碑：完成一次小型位内存模拟。通过类型名查找位宽，在指定地址读取位序列，再把第一位作为最低位解释成无符号整数。

| 文件 | 内容 | 运行情况 |
| --- | --- | --- |
| `virtual_machine.py` | 三个小内存块、预先拼接的数据副本、类型登记、位宽累加、边界检查 | 末尾的未定义类型用例会抛出预期异常 |
| `virtual_memory_experiment.py` | 区分文件偏移、每个进程的虚拟地址与模拟页框；共享读写、缺页和错误示例 | 可直接运行 |
| `memory_alias.py` | 同一临时文件建立两个真实 mmap，观察不同虚拟地址下的共享读写 | 可直接运行 |
| `memory_alias2.py` | 比较共享映射与私有复制映射 | 可直接运行；具体可见性由操作系统映射语义决定 |

```console
python -X utf8 01_memory_simulation/virtual_memory_experiment.py
python -X utf8 01_memory_simulation/memory_alias.py
python -X utf8 01_memory_simulation/memory_alias2.py
```

## 第一轮模型的边界

- 第四个列表是前三块内容的独立副本，尚无动态同步机制。
- 自定义类型目前只保存名称与总位宽，尚无成员布局与成员解码。
- 原始边界检查尚未覆盖负地址等所有输入。
- 分页模型使用 4 字节的模拟页，页框编号由 Python 模型管理；真实 mmap 示例不读取物理页框编号。
- 分页模型中的写入只修改驻留页框，未实现写回文件。

这些文件保留各阶段实验的规则，未来由第三模块明确如何调用和扩展内存接口。
