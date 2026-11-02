dictionary = ['你','好','再','见','p','r','i','n','t']
code = ['0000','0001','0010','0011','1000','1001','1010','1011','1100']
file_suffix = ['exe','txt']

def read_file(file_name_binary,suffix):
    file_len = 7
    if suffix == 'txt':
        for i in range(file_len):
            print(read_byte(file_name_binary,4*i))
    if suffix == 'exe':
        source_code = ''
        for i in range(file_len):
            source_code = source_code + read_byte(file_name_binary,4*i)
        if source_code[0] == 'p':
            print("你好")
        
def read_byte(file_binary,add):
    binary_to_be_read = ""
    for i in range(4):
        binary_to_be_read = binary_to_be_read + file_binary[add + i]
    return dictionary[code.index(binary_to_be_read)]

hello_file = "print你好"
hello_file_binary = '1000100110101011110000000001'

read_file(hello_file_binary,'exe')