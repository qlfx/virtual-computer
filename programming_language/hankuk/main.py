"""中枢入口：读取 UTF-8 的 .kr 文件，交给韩语解释器执行。"""
import argparse
import sys
from pathlib import Path

from programming_language.hankuk.hankuk_quine_interpret import compile as run_code


def run_file(path):
    path = Path(path)
    if path.suffix.lower() != ".kr":
        raise ValueError("请选择后缀为 .kr 的韩语代码文件。")

    # utf-8-sig 同时接受有、无 BOM 的 UTF-8 文件。
    # newline="" 保留引用数据中的原始换行；不 strip() 源代码。
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        code = file.read()

    # 解释器本身会打印；返回值供验证使用，不能再 print 一遍。
    return run_code(code)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program", type=Path, help="要运行的 .kr 文件路径")
    args = parser.parse_args(argv)

    try:
        run_file(args.program)
    except (OSError, UnicodeError, SyntaxError, NameError, ValueError) as error:
        print(f"{args.program}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
