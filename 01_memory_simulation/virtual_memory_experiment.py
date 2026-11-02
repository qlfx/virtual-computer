"""A tiny model of file offsets, per-process virtual addresses, and frames.

Frame numbers and page faults here are simulated. Writes change a resident
frame only; flushing the frame back to the file is outside this tiny model.
See memory_alias.py for a real mmap experiment; Python does not expose its
physical frame numbers.
"""

PAGE_SIZE = 4
FILE_BYTES = bytearray([10, 20, 30, 40, 50, 60, 70, 80])

# (process, virtual page) -> file page
MAPPINGS = {("A", 3): 1, ("B", 1): 1, ("C", 5): 0, ("D", 2): 2}

# File page 1 is already in simulated physical frame 2.
RESIDENT = {1: 2}
FRAMES = {2: bytearray(FILE_BYTES[4:8])}
next_frame = 3


def locate(process, virtual_address):
    """Return the three coordinates of one byte and its resident frame."""
    global next_frame

    if virtual_address < 0:
        raise ValueError("虚拟地址不能为负")
    virtual_page, offset = divmod(virtual_address, PAGE_SIZE)
    key = (process, virtual_page)
    if key not in MAPPINGS:
        raise ValueError(f"进程 {process} 的虚拟页 {virtual_page} 未映射")

    file_page = MAPPINGS[key]
    file_offset = file_page * PAGE_SIZE + offset
    if (file_page + 1) * PAGE_SIZE > len(FILE_BYTES):
        raise ValueError(f"文件页 {file_page} 超出文件范围")

    if file_page not in RESIDENT:
        frame = next_frame
        next_frame += 1
        start = file_page * PAGE_SIZE
        FRAMES[frame] = bytearray(FILE_BYTES[start : start + PAGE_SIZE])
        RESIDENT[file_page] = frame
        print(f"  模拟缺页：文件偏移 {start}～{start + PAGE_SIZE - 1} -> 页框 {frame}")

    return virtual_page, offset, file_offset, RESIDENT[file_page]


def read(process, virtual_address):
    virtual_page, offset, file_offset, frame = locate(process, virtual_address)
    value = FRAMES[frame][offset]
    print(
        f"{process} 虚拟地址 {virtual_address} = 虚拟页 {virtual_page} + 页内偏移 {offset}"
        f" -> 文件偏移 {file_offset} -> 模拟页框 {frame} + 偏移 {offset} -> {value}"
    )
    return value


def write(process, virtual_address, value):
    if not 0 <= value <= 255:
        raise ValueError("写入值必须是一个字节")
    virtual_page, offset, file_offset, frame = locate(process, virtual_address)
    FRAMES[frame][offset] = value
    print(
        f"{process} 写入虚拟地址 {virtual_address}（虚拟页 {virtual_page}，"
        f"文件偏移 {file_offset}，模拟页框 {frame} + 偏移 {offset}）= {value}"
    )


if __name__ == "__main__":
    assert read("A", 14) == 70
    assert read("B", 6) == 70  # Different virtual address, same resident frame.
    write("A", 14, 99)
    assert read("B", 6) == 99
    assert read("C", 21) == 20  # A simulated page fault loads file page 0.

    for process, address in [("A", 0), ("D", 8)]:
        try:
            read(process, address)
        except ValueError as error:
            print(f"预期错误：{error}")
