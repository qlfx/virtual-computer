import sys
sys.path.append(r"D:\Self_Products\memory\memory_simulation")
import virtual_machine

Types = ["Int","Char","Bool"]  #这个应该是数据解读规律，储存在一个特殊的地方
Type_Size = [4,8,1]

m1 = virtual_machine.Memory(8)
m2 = virtual_machine.Memory(8)
Memories = [m1,m2]

#这部分是变量名、类型、储存地址的信息，储存在另一个地方
variable_name_list = []
variable_type_list = []
variable_address_list = []

#这部分储存已有类型，用于类型检验
type_structure_list = [["Int"],["Char"],["Bool"]]

class Memory_Tool:
    def __init__(self):
        pass

    def read_data(self,memory,add,type_size):
        data = []
        for i in range(type_size):
            data.append(memory.memory_physical[add + i])
        return data

    def write_data(self,memory,add,type_size,bit_stream):
        for i in range(type_size):
            memory.memory_physical[add + i] = bit_stream[i]

    def get_address_from_variable_name(self,variable_name):
        return variable_address_list[variable_name_list.index(variable_name)]

    def find_available_space(self,size,memory):
        if size > memory.available_size:
            # print("内存溢出")
            return False
        add = memory.memory_size - memory.available_size
        return memory,add