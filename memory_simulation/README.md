# 位内存

[virtual_machine.py](virtual_machine.py) 定义 `Memory(bits)`。每个对象拥有独立的比特列表、总容量和剩余容量。地址和容量都以 bit 为单位。

实验的容量由硬件配置指定。读写与空间分配交给[内存管理层](../memory_for_caculation/README.md)。
