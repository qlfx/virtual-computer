variable_lists = []
addition = []

Type_List = []      #记录类型
Value_List = []

commutative = "전(x,Z):전(y,Z):는(더(x,y),더(y,x))"
proof = "말(2,Z)x:말(3,Z)y with commutative(x,y) -> 는(더(2,3),더(3,2))"

def check_proof(theorem_term,conclusion_term):
    theorem_term_list = list(theorem_term)
    conclusion_term_list = list(conclusion_term)
    for i in range(len(theorem_term)):
        p = i-1
        if theorem_term_list[p] == 'x':
            theorem_term_list[p] = '2'
        if theorem_term_list[p] == 'y':
            theorem_term_list[p] = '3'
    if theorem_term_list == conclusion_term_list:
        print("Valid proof")
        return True
    return False

def parse_theorem(theorem):
    for i in range(len(theorem)):
        if theorem[i] == '전':
            Type_List.append(theorem[i + 4])
        if theorem[i] == '는':
            term = theorem[i:]
            return term

def parse_result(proof):
    for i in range(len(proof)):
        if proof[i] == '말':
            if proof[i + 4] == Type_List[0]:
                Value_List.append(proof[i + 2])
        if proof[i] == '는':
            term = proof[i:]
            return term

check_proof(parse_theorem(commutative),parse_result(proof))