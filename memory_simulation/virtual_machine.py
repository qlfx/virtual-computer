class Memory:
    def __init__(self,bits):
        self.memory_size = bits
        self.memory_physical = create_a_memory(self.memory_size)
        self.available_size = bits
        
def create_a_memory(bits):
    memory = []
    for i in range(bits):
            memory.append(0)
    return memory