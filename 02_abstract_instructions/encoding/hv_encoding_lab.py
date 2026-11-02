"""Horizontal/vertical geometry encoding lab. Standard library only.
Read main() last: codecs operate on geometry, never on a character ID.
Coordinates are integer samples in [0,100]; H goes right, V goes down.
"""
import argparse
import inspect
import json
import random
import statistics
import timeit
from fractions import Fraction
from pathlib import Path

SAMPLES = {
    "干": [[0,30,25,70,25],[0,15,50,85,50],[1,50,25,50,85]],
    "士": [[0,15,45,85,45],[1,50,15,50,80],[0,30,80,70,80]],
    "土": [[0,30,45,70,45],[1,50,15,50,80],[0,15,80,85,80]],
    "十": [[0,15,50,85,50],[1,50,15,50,85]],
}

def validate_rows(rows):
    if not 1 <= len(rows) <= 255:
        raise ValueError("Need 1..255 strokes.")
    for row in rows:
        if len(row) != 5 or any(type(x) is not int for x in row):
            raise ValueError("A stroke has five integer fields.")
        kind, x, y, u, v = row
        if any(not 0 <= a <= 100 for a in row[1:]):
            raise ValueError("Coordinates must lie in [0,100].")
        if not ((kind == 0 and y == v and x < u) or
                (kind == 1 and x == u and y < v)):
            raise ValueError("Only rightward H and downward V are supported.")

def endpoint(kind, x, y, length):
    return [kind, x, y, x+length if kind == 0 else x,
            y if kind == 0 else y+length]

class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def get(self, width):
        if self.pos + width > 8*len(self.data):
            raise ValueError("Truncated payload.")
        result = 0
        for _ in range(width):
            byte, bit = divmod(self.pos, 8)
            result = (result << 1) | ((self.data[byte] >> (7-bit)) & 1)
            self.pos += 1
        return result

def begin(data, expected):
    r = Reader(data)
    if r.get(2) != expected:
        raise ValueError("Wrong format selector.")
    n = r.get(8)
    if not n:
        raise ValueError("Empty glyph.")
    return r, n

def finish(r, rows):
    used = r.pos
    if len(r.data) != (used+7)//8:
        raise ValueError("Unexpected extra bytes.")
    if r.get((-used) % 8):
        raise ValueError("Nonzero padding.")
    validate_rows(rows)
    return rows

def decode_endpoints(data):
    r, n = begin(data, 0)
    rows = [[r.get(1), r.get(7), r.get(7), r.get(7), r.get(7)]
            for _ in range(n)]
    return finish(r, rows)

def decode_axis(data):
    r, n = begin(data, 1)
    rows = []
    for _ in range(n):
        kind, x, y, length = r.get(1), r.get(7), r.get(7), r.get(7)
        rows.append(endpoint(kind, x, y, length))
    return finish(r, rows)

def decode_relative(data):
    r, n = begin(data, 2)
    ax, ay, unit = r.get(7), r.get(7), r.get(7)
    if not unit:
        raise ValueError("Zero reference length.")
    rows, references, seen_vertical = [], 0, False
    for _ in range(n):
        tag = r.get(2)
        if tag == 0:
            if seen_vertical:
                raise ValueError("Reference must be the first vertical.")
            rows.append(endpoint(1, ax, ay, unit))
            references += 1
            seen_vertical = True
        elif tag in (1, 2):
            dx, dy, length = r.get(8)-100, r.get(8)-100, r.get(7)
            rows.append(endpoint(tag-1, ax+dx, ay+dy, length))
            seen_vertical = seen_vertical or tag == 2
        else:
            raise ValueError("Reserved stroke tag.")
    if references != 1:
        raise ValueError("Exactly one reference is required.")
    return finish(r, rows)

DECODERS = (decode_endpoints, decode_axis, decode_relative)
NAMES = ("endpoints", "axis", "relative")

def encode(rows, mode):
    validate_rows(rows)
    fields = []
    def put(value, width):
        if not 0 <= value < 1 << width:
            raise ValueError("Field outside its bit width.")
        fields.append(format(value, "0%db" % width))
    put(mode, 2)
    put(len(rows), 8)
    ref = None
    if mode == 2:
        ref = next((i for i, row in enumerate(rows) if row[0] == 1), None)
        if ref is None:
            raise ValueError("Relative v1 needs at least one vertical.")
        _, ax, ay, _, bottom = rows[ref]
        put(ax, 7)
        put(ay, 7)
        put(bottom-ay, 7)
    elif mode not in (0, 1):
        raise ValueError("Unknown codec.")
    for i, (kind, x, y, u, v) in enumerate(rows):
        length = u-x if kind == 0 else v-y
        if mode == 0:
            put(kind, 1)
            for value in (x, y, u, v):
                put(value, 7)
        elif mode == 1:
            for value, width in ((kind,1),(x,7),(y,7),(length,7)):
                put(value, width)
        elif i == ref:
            put(0, 2)
        else:
            # dx/unit, dy/unit, length/unit share the denominator in the header.
            put(kind+1, 2)
            put(x-ax+100, 8)
            put(y-ay+100, 8)
            put(length, 7)
    bits = "".join(fields)
    padded = bits + "0"*((-len(bits)) % 8)
    data = bytes(int(padded[i:i+8],2) for i in range(0,len(padded),8))
    return data, len(bits)

def relative_model(rows):
    ref = next(i for i, row in enumerate(rows) if row[0] == 1)
    _, ax, ay, _, bottom = rows[ref]
    unit = bottom-ay
    model = []
    for i, (kind,x,y,u,v) in enumerate(rows):
        if i == ref:
            model.append({"template":"V-reference"})
        else:
            length = u-x if kind == 0 else v-y
            model.append({"template":"H" if kind == 0 else "V",
                          "dx":str(Fraction(x-ax,unit)),
                          "dy":str(Fraction(y-ay,unit)),
                          "length":str(Fraction(length,unit))})
    return {"pose":{"origin":[ax,ay],"unit":unit},"strokes":model}

def self_check():
    rng = random.Random(20261027)
    cases = list(SAMPLES.values())
    for _ in range(100):
        rows = []
        for i in range(rng.randint(1,12)):
            kind = 1 if i == 0 else rng.randrange(2)
            x, y = rng.randrange(100), rng.randrange(100)
            length = rng.randint(1,100-(x if kind == 0 else y))
            rows.append(endpoint(kind,x,y,length))
        cases.append(rows)
    for rows in cases:
        for mode, decoder in enumerate(DECODERS):
            data, used = encode(rows,mode)
            assert decoder(data) == rows
            n = len(rows)
            expected = (10+29*n, 10+22*n, 25*n+8)[mode]
            assert used == expected
    rejected = 0
    for rows in ([], [[0,0,0,10,1]], [[1,0,10,0,0]]):
        try:
            encode(rows,0)
        except ValueError:
            rejected += 1
    try:
        encode([[0,0,0,10,0]],2)
    except ValueError:
        rejected += 1
    for mode, decoder in enumerate(DECODERS):
        data, used = encode(SAMPLES["士"],mode)
        for bad in (data[:-1], data+b"\x00",
                    data[:-1]+bytes([data[-1] | 1])):
            try:
                decoder(bad)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError("Invalid payload accepted.")
    assert rejected == 13
    # This proxy is sensitive to relative lengths: ignoring them merges shi/tu.
    def without_lengths(char):
        strokes = relative_model(SAMPLES[char])["strokes"]
        return [stroke if stroke["template"] == "V-reference" else
                {"template":stroke["template"], "dy":stroke["dy"],
                 "center_dx":str(Fraction(stroke["dx"])+Fraction(stroke["length"])/2)}
                for stroke in strokes]
    assert without_lengths("士") == without_lengths("土")
    # Normalized relations are invariant to an integer translation and scaling.
    for rows in SAMPLES.values():
        transformed = [[k,2*x+7,2*y+3,2*u+7,2*v+3] for k,x,y,u,v in rows]
        assert relative_model(rows)["strokes"] == relative_model(transformed)["strokes"]
    return {"roundtrips":len(cases)*3, "invalid_cases_rejected":rejected,
            "normalized_transform_checks":len(SAMPLES),
            "length_omission_collision":True}

def make_report():
    checks = self_check()
    common_objects = (Reader, begin, finish, validate_rows, endpoint)
    shared_bytes = sum(len(inspect.getsource(obj).encode("utf-8"))
                       for obj in common_objects)
    codecs = []
    samples = []
    for mode, decoder in enumerate(DECODERS):
        payloads = [encode(rows,mode)[0] for rows in SAMPLES.values()]
        def batch():
            for data in payloads:
                decoder(data)
        seconds = statistics.median(timeit.repeat(batch,number=1000,repeat=5))
        codecs.append({
            "name":NAMES[mode],
            "decoder_function_utf8_bytes":len(inspect.getsource(decoder).encode("utf-8")),
            "shared_helper_utf8_bytes":shared_bytes,
            "decode_us_per_glyph":seconds/1000/len(payloads)*1e6,
            "timing_scope":"bit parsing + geometry reconstruction + validation; excludes rendering",
            "time_order_fixed_7bit_coordinates":"Theta(n)",
            "reconstruction_additions_per_glyph":"0" if mode == 0 else ("n" if mode == 1 else "3*n-2"),
        })
    for char, rows in SAMPLES.items():
        item = {"label":char, "strokes":rows, "relative_model":relative_model(rows),
                "encodings":[]}
        for mode, decoder in enumerate(DECODERS):
            data, used = encode(rows,mode)
            restored = decoder(data)
            item["encodings"].append({"name":NAMES[mode],"meaningful_bits":used,
                "stored_bytes":len(data),"hex":data.hex(),"decoded":restored,
                "exact_roundtrip":restored == rows})
        samples.append(item)
    for mode, codec in enumerate(codecs):
        codec["total_meaningful_bits"] = sum(s["encodings"][mode]["meaningful_bits"] for s in samples)
        codec["total_stored_bytes"] = sum(s["encodings"][mode]["stored_bytes"] for s in samples)
        codec["source_plus_payload_proxy_bits"] = 8*(shared_bytes+codec["decoder_function_utf8_bytes"])+codec["total_meaningful_bits"]
    return {"domain":"ideal H/V segments, integer coordinates 0..100; stroke order retained",
        "provenance":"Hand-defined four-glyph samples from the earlier demo, not original Make Me a Hanzi medians.",
        "format":"2-bit selector + 8-bit count; coordinate=7 bits; relative adds 21-bit pose and 2-bit tags; offsets use 8-bit biased integers.",
        "lossless_target":"exact original endpoints including absolute position and scale",
        "scope":"relative v1 requires a vertical; supports additional verticals; no graph constraint solver",
        "timing_environment":"Python string-free bit reader; numbers are implementation-specific, not an optimality proof",
        "source_length_scope":"UTF-8 decoder function plus listed common helpers; Python/builtins and file framing convention are assumed shared; not Kolmogorov complexity",
        "checks":checks,"codecs":codecs,"samples":samples}

def make_svg(report):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="740" viewBox="0 0 960 740">',
             '<rect width="960" height="740" fill="#f5f7fb"/>',
             '<style>text{font-family:Arial,sans-serif;fill:#23334b}line{stroke:#263e65;stroke-width:3;stroke-linecap:round}</style>',
             '<text x="30" y="34" font-size="22">Same geometry, three binary encodings</text>']
    for col, codec in enumerate(report["codecs"]):
        parts.append(f'<text x="{100+col*300}" y="68" font-size="18">{codec["name"]}</text>')
    for row, sample in enumerate(report["samples"]):
        y = 90+row*155
        parts.append(f'<text x="20" y="{y+60}" font-size="22">{sample["label"]}</text>')
        for col, encoding in enumerate(sample["encodings"]):
            x = 70+col*300
            parts.append(f'<rect x="{x}" y="{y}" width="260" height="140" rx="10" fill="white"/>')
            parts.append(f'<g transform="translate({x+80},{y+5})">')
            for _,x1,y1,x2,y2 in encoding["decoded"]:
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
            parts.append('</g>')
            parts.append(f'<text x="{x+22}" y="{y+128}" font-size="15">{encoding["meaningful_bits"]} bits / {encoding["stored_bytes"]} bytes</text>')
    parts.append('</svg>')
    return "\n".join(parts)

README = """# 横竖编码与复杂度实验
运行：python hv_encoding_lab.py
保存结果：python hv_encoding_lab.py --output hv_complexity
本程序只用标准库；字符名称只用于显示和组织样本，解码器不读取字符名。

## 比较对象
样本是此前手工定义的干、士、土、十理想线段，不是 Make Me a Hanzi 的真实中线。
三个解码器都精确恢复同样的整数端点、绝对位置、大小和笔顺。暂不删除书写细节。
坐标域0..100，向右为x正、向下为y正；H向右，V向下；每字1..255笔。
相对编码需要至少一条竖，以第一条竖为参照；允许额外的横竖。

## 三种二进制格式
所有格式开头都有2位格式号与8位笔画数。
A endpoints：每笔1位方向+4个7位端点坐标。总长10+29n位。
B axis：每笔1位方向+起点x/y各7位+长度7位。总长10+22n位。
C relative：额外保存参考竖起点x/y及长度L，各7位。
每笔2位标签：00参考竖，01横，10其他竖；11保留。
参考竖不带额外参数，其他笔带起点相对偏移dx/dy各8位、长度7位。
偏移用dx+100、dy+100保存；合法区间-100..100。
相对参数在概念上是dx/L、dy/L、length/L，共用头部的分母L。
总长2+8+21+2n+23(n-1)=25n+8位。
这是一种简单、明确、可逆的表示，并未声称是最佳相对编码。
位流末尾补零到字节边界；结果分别列出有效位数和实际字节数。
2位格式号仅用于选择解码器，不传输解码规则本身；规则成本另计。

## 怎么理解复杂度
1. 数据码长：给定格式下实际使用的位数；JSON字符数不是理论信息量。
2. 解码描述长度：报告Python解码函数UTF-8字节数、共同helper字节数。
   这是可复现的工程代理，不是最短算法的长度。注释、语言、写法都会影响它。
   解释器、内置函数、字节流输入边界、输出列表约定被视为共同背景。
   source_plus_payload_proxy_bits 只是固定背景下的一个候选描述上界。
3. 计算成本：报告解析、重建和校验的计时，排除画图；运行时间随机器变化。
   三种解码器读取每笔一次、输出每笔一次，在固定7位坐标模型中都是Theta(n)。
   至少输出n条线段需要Omega(n)，所以这里达到的是时间阶上的最优。
   仅重建端点所需加法数分别为0、n、3n-2；不含解析、寻址与校验。
   输出列表空间均Theta(n)；若逐笔流式输出，固定精度下额外工作空间可为O(1)。
   若坐标精度也变化，应另引入q，分析输入位数和整数运算成本。
4. 统计熵：H(X)=-sum p(x)log2 p(x)，需要先指定随机变量和分布。
   四个字等概率、且已有字形字典时，选择字形需要2位。
   这2位没有包含字典及其绘图规则，不能直接与独立几何编码比较。
   无损可逆改写不改变同一个随机对象的熵；它可以减少具体格式的冗余。
5. 最短程序：固定通用机后，生成某对象的最短程序长度称Kolmogorov复杂度。
   它一般不可计算，不能用这个实验求出真正最短解码器。
6. 共同模型成本：L(规则)+sum L(字形|规则)。规则可被整个字库共享。
   这是借用MDL的两部分描述思路；当前没有做完整统计模型选择。
   不能既使用免费字典/解码器，又把另一个方案恢复几何的全部成本都算进去。

## 本轮结果的边界
相对编码胜过保存四个端点坐标的格式，但输给已经删除横竖冗余的axis格式。
这与我们选择的位宽、参考头部、标签及小样本范围有关，不证明相对编码普遍较差。
它说明：抽象表达更统一，不保证位流更短；规则共享也不保证运行时间增长一个数量级。
JSON中的分数方便人理解，实际位流里分母、符号、参考姿态均有明确成本。
当前没有推断相交矩阵、做数值约束求解或学习真实中线的笔画类别。
直接放置模板通常是线性解码；纯关系编码若需要解约束，要另行分析。
若只恢复平移/尺度等价类，两边都必须改用这一共同目标再比较。
真实中线归类为横竖可能丢失细节，需要另外报告误差；不能把删掉的信息算作无损压缩。

## 推荐阅读顺序
SAMPLES -> relative_model -> encode -> decode_axis -> decode_relative -> make_report
结果文件：results.json（位数/十六进制/时间/源码代理/解码结果），comparison.svg（几何对照）。
自检包含四字、100个随机横竖图形的312次往返、13个非法输入、
四次平移缩放归一化检验，以及以横的中心描述位置并删除相对长度后士/土发生碰撞的检验。
这些检查不证明任意真实汉字能唯一编码。

参考：
Shannon, A Mathematical Theory of Communication:
https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf
Vitanyi, How incomputable is Kolmogorov complexity?:
https://arxiv.org/abs/2002.07674
Grunwald, A Tutorial Introduction to the Minimum Description Length Principle:
https://arxiv.org/abs/math/0406077
"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = make_report()
    for sample in report["samples"]:
        counts = ", ".join(f'{e["name"]}={e["meaningful_bits"]}b/{e["stored_bytes"]}B'
                           for e in sample["encodings"])
        print(json.dumps(sample["label"],ensure_ascii=True), counts)
    for codec in report["codecs"]:
        print(codec["name"], "total", codec["total_meaningful_bits"], "bits;",
              "decoder function", codec["decoder_function_utf8_bytes"], "UTF-8 bytes;",
              "median", round(codec["decode_us_per_glyph"],2), "us/glyph")
    print("CHECKS", json.dumps(report["checks"]))
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output/"results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        (args.output/"comparison.svg").write_text(make_svg(report),encoding="utf-8")
        (args.output/"README.md").write_text(README,encoding="utf-8")

if __name__ == "__main__":
    main()
