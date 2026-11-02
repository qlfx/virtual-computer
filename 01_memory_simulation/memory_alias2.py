
import mmap
import tempfile

with tempfile.TemporaryFile() as f:
    f.write(b"ABCD")
    f.truncate(4096)
    f.flush()

    with (
        mmap.mmap(f.fileno(), 4096,
                  access=mmap.ACCESS_WRITE) as a,
        mmap.mmap(f.fileno(), 4096,
                  access=mmap.ACCESS_WRITE) as b,
        mmap.mmap(f.fileno(), 4096,
                  access=mmap.ACCESS_COPY) as c
    ):
        print("Initial:", a[:4], b[:4], c[:4])

        # c 修改自己的私有视图
        c[0] = ord("X")

        # a 修改共享文件内容
        a[1] = ord("Y")

        print("After:", a[:4], b[:4], c[:4])
