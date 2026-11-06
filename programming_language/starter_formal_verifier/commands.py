import sys
sys.path.append(r"D:\Self_Products\memory\memory_for_caculation")
sys.path.append(r"D:\Self_Products\memory\memory_simulation")
sys.path.append(r"D:\Self_Products\memory\type_realizer")
import memory_operator as mo
import virtual_machine
import type_realizer as tr

type_tool = tr.Type_Operator()
memory_tool = mo.Memory_Tool()

class Formal_Verifier_Command_Set:
    def __init__(self) -> None:
        pass

    def declare_a_variable(self,type_name,variable_name):
        type_tool.simple_type_check(type_name)
        if variable_name in mo.variable_name_list:
            print("已存在变量：",variable_name)
            sys.exit()
        size = mo.Type_Size[mo.Types.index(type_name)]

        #内存检查并不能把两块内存拼到一起
        for i in range(len(mo.Memories)):
            result = memory_tool.find_available_space(size,mo.Memories[i])
            if result != False:
                mo.variable_name_list.append(variable_name)
                mo.variable_type_list.append(type_name)
                mo.Memories[i].available_size = mo.Memories[i].available_size - size
                mo.variable_address_list.append(result)
                return result
        print("内存溢出")
        sys.exit()

f = Formal_Verifier_Command_Set()
type_tool.define_a_new_type(["Int","Bool","Bool"],"zlfx")
print(f.declare_a_variable('Bool','b'))
print(f.declare_a_variable('Bool','d'))
print(f.declare_a_variable('zlfx','f'))
print(mo.variable_name_list)
print(mo.Type_Size)
print(mo.Types)
print(mo.variable_address_list)
print(mo.type_structure_list)