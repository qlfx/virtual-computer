import virtual_machine

memory1 = virtual_machine.Memory_Physical[3]    # 地址列表示例；实际读写的数据由 vm 管理。


def translate_Korean_codes_to_commands(Korean_codes, vm):
    command_set = []
    letter_set = parse_Korean_codes(Korean_codes)
    for letters in letter_set:
        # 每个音节按初声、中声、终声的顺序执行。
        for letter in letters:
            command = parse_letter_to_command(letter, vm)
            if command is not None:
                command_set.append(command)
    # 沿用原来的框架：翻译时直接执行，返回已经执行的命令名。
    return command_set


def parse_Korean_codes(Korean_codes):
    letter_set = []
    for Korean_code in Korean_codes:
        letter_set.append(parse_single_Korean_code(Korean_code))
    return letter_set


def parse_single_Korean_code(Korean_code):
    # 输入为一个现代预组合韩语音节（가～힣），输出兼容字母三元组。
    # 无终声和实际终声 ㅇ 都记为 ㅇ，这是本语言的约定。
    if not isinstance(Korean_code, str) or len(Korean_code) != 1:
        raise ValueError("请传入一个韩语音节。")

    code_index = ord(Korean_code) - 0xAC00
    if not 0 <= code_index < 19 * 21 * 28:
        raise ValueError(f"{Korean_code!r} 不是 가～힣 范围内的韩语音节。")

    initial_letters = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    middle_letters = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
    final_letters = (
        "", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ",
        "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ",
        "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ",
    )

    initial_index = code_index // (21 * 28)
    middle_index = (code_index % (21 * 28)) // 28
    final_index = code_index % 28

    initial = initial_letters[initial_index]
    middle = middle_letters[middle_index]
    final = final_letters[final_index] or "ㅇ"
    return (initial, middle, final)


vm = virtual_machine.Memory(0)
vm.init_memory()


def parse_letter_to_command(letter, vm):
    if letter == "ㅏ":
        vm.move_to_right()
        return "move_to_right"
    if letter == "ㅓ":
        vm.move_to_left()
        return "move_to_left"
    if letter == "ㄹ":
        vm.wright_zero()
        return "wright_zero"
    if letter == "ㅂ":
        vm.wright_one()
        return "wright_one"
    # ㅇ、ㅣ 以及其他尚未定义指令的字母，目前都不执行操作。
    return None

if __name__ == "__main__":
    Korean_codes = "바발어"
    print("韩语分解：", parse_Korean_codes(Korean_codes))
    print("执行前：", vm.memory_virtual, "指针：", vm.memory_pointer)
    commands = translate_Korean_codes_to_commands(Korean_codes, vm)
    print("执行指令：", commands)
    print("执行后：", vm.memory_virtual, "指针：", vm.memory_pointer)
