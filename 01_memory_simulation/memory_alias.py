
import mmap
import tempfile
import ctypes

# 1. 建立临时文件，大小为 4096 字节
with tempfile.TemporaryFile() as f:
    f.truncate(4096)

    # 2. 对同一个文件建立两份可写内存映射
    with mmap.mmap(f.fileno(), 4096,
                   access=mmap.ACCESS_WRITE) as a:
        with mmap.mmap(f.fileno(), 4096,
                       access=mmap.ACCESS_WRITE) as b:

            # 3. 获取两个映射区域首字节的虚拟地址
            addr_a = ctypes.addressof(
                ctypes.c_char.from_buffer(a)
            )
            addr_b = ctypes.addressof(
                ctypes.c_char.from_buffer(b)
            )

            print("A address:", hex(addr_a))
            print("B address:", hex(addr_b))
            print("Same address?", addr_a == addr_b)

            # 4. 通过 A 写入
            a[0:4] = b"ZLFX"

            # 5. 通过 B 读取
            print("Read from B:", b[0:4])

            # 6. 通过 B 修改
            b[1] = ord("!")

            # 7. 再通过 A 读取
            print("Read from A:", a[0:4])
