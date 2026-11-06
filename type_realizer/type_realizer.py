import sys
sys.path.append(r"D:\Self_Products\memory\memory_for_caculation")
sys.path.append(r"D:\Self_Products\memory\memory_simulation")
import memory_operator
import virtual_machine

class Type_Operator(memory_operator.Memory_Tool):
    # def __init__(self,type_name):
    #     self.type_name = type_name
    #     self.type_size = memory_operator.Type_Size[memory_operator.Types.index(type_name)]
    def __init__(self):
        pass

    def simple_type_check(self,type_name):
        if type_name not in memory_operator.Types:
            print("未定义的类型：",type_name)
            sys.exit()
        return True

    def define_a_new_type(self,old_type_names,new_type_name):
        if new_type_name == '':
            print("类型名称不能为空")
            sys.exit()
        if old_type_names == []:
            print("使用的类型列表不能为空")
            sys.exit()
        if new_type_name in memory_operator.Types:
            print("已定义的类型：",new_type_name)
            sys.exit()
        gate = True
        for type in old_type_names:
            gate = gate and self.simple_type_check(type)
        
        def get_new_type_size():
            total_size = 0
            for type in old_type_names:
                total_size = total_size + memory_operator.Type_Size[memory_operator.Types.index(type)]
            return total_size
        
        if gate == True:
            memory_operator.Types.append(new_type_name)
            memory_operator.Type_Size.append(get_new_type_size())
            type_structure = []
            for type in old_type_names:
                type_structure.append(type)
            memory_operator.type_structure_list.append(type_structure)
            return True

        sys.exit()