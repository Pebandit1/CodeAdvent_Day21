def get_codes():
    codes = []
    with open("input.txt", "r") as file :
        for line in file:
            codes.append(line.removesuffix("\n"))
    return codes

def add_to_result(prev_char, delta, new_char, height, result):
    result.append((prev_char, new_char, height - 1))
    for _ in range(1,delta):
        result.append((new_char,new_char, height - 1))

def code_to_input(curr):
    CONVERT = {"7":(0,0),"8":(0,1), "9":(0,2), "4":(1,0),"5":(1,1),"6":(1,2),"1":(2,0),"2":(2,1),"3":(2,2), "0":(3,1), "A":(3,2)}
    curr_pos = CONVERT[curr[0]]
    end_pos = CONVERT[curr[1]]
    prev_input = "A"
    result = []

    if(end_pos[1] < curr_pos[1]):
        delta = curr_pos[1] - end_pos[1]
        add_to_result(prev_input, delta, "<", curr[2], result)
        prev_input = "<"
        curr_pos = (curr_pos[0], end_pos[1])

    if(end_pos[0] == 3 and curr_pos[1] == 0 and  end_pos[1] > curr_pos[1]):
        delta = end_pos[1] - curr_pos[1]
        add_to_result(prev_input, delta, ">", curr[2], result)
        prev_input = ">"
        curr_pos = (curr_pos[0], end_pos[1])

    if(end_pos[0] < curr_pos[0]):
        delta = curr_pos[0] - end_pos[0]
        add_to_result(prev_input, delta, "^", curr[2], result)
        prev_input = "^"
        curr_pos = (end_pos[0], curr_pos[1])
        
    if(end_pos[0] > curr_pos[0]):
        delta = end_pos[0] - curr_pos[0]
        add_to_result(prev_input, delta, "v", curr[2], result)
        prev_input = "v"
        curr_pos = (end_pos[0], curr_pos[1])
        
    if(end_pos[1] > curr_pos[1]):
        delta = end_pos[1] - curr_pos[1]
        add_to_result(prev_input, delta, ">", curr[2], result)
        prev_input = ">"
        curr_pos = (curr_pos[0], end_pos[1])
        
    result.append((prev_input, "A", curr[2] - 1))
    return result

def input_to_more_input(curr):
    CONVERT = {"<":(1,0),"^":(0,1), "A":(0,2), "v" : (1,1), ">":(1,2)}
    curr_pos = CONVERT[curr[0]]
    end_pos = CONVERT[curr[1]]      
    prev_input = "A"
    result = []

    if(end_pos[1] == 0 and curr_pos[0] == 0 and end_pos[0] > curr_pos[0]):
        delta = end_pos[0] - curr_pos[0]
        add_to_result(prev_input, delta, "v", curr[2], result)
        prev_input = "v"
        curr_pos = (end_pos[0], curr_pos[1])

    if(end_pos[1] < curr_pos[1]):
        delta = curr_pos[1] - end_pos[1]
        add_to_result(prev_input, delta, "<", curr[2], result)
        prev_input = "<"
        curr_pos = (curr_pos[0], end_pos[1])

    if(end_pos[0] < curr_pos[0]):
        delta = curr_pos[0] - end_pos[0]
        add_to_result(prev_input, delta, "^", curr[2], result)
        prev_input = "^"
        curr_pos = (end_pos[0], curr_pos[1])
        
    if(end_pos[0] > curr_pos[0]):
        delta = end_pos[0]  -curr_pos[0]
        add_to_result(prev_input, delta, "v", curr[2], result)
        prev_input = "v"
        curr_pos = (end_pos[0], curr_pos[1])
        
    if(end_pos[1] > curr_pos[1]):
        delta = end_pos[1] - curr_pos[1]
        add_to_result(prev_input, delta, ">", curr[2], result)
        prev_input = ">"
        curr_pos = (curr_pos[0], end_pos[1])
        
    result.append((prev_input, "A", curr[2] - 1))
    return result

NB_ROBOTS = 25
CHARACTERS = ["A",">","<","v","^"]

codes = get_codes()
total = 0
unique_cost = dict()

for char1 in CHARACTERS:
    for char2 in CHARACTERS:
        unique_cost[(char1,char2, 0)] = 1

for i in range(1,NB_ROBOTS):
    for char1 in CHARACTERS:
        for char2 in CHARACTERS: 
            curr = (char1, char2, i)
            operations = input_to_more_input(curr)
            nb_inputs = 0
            for op in operations:
                nb_inputs += unique_cost[op]
            unique_cost[curr] = nb_inputs

for code in codes:
    operations = []
    operations.append(("A", code[0], NB_ROBOTS))
    for i in range(1,len(code)):
        operations.append((code[i-1], code[i], NB_ROBOTS))
    total_cost = 0

    for op in operations:
        lower_operations = code_to_input(op)
        for lower in lower_operations:
            total_cost += unique_cost[lower]
        
    print(total_cost, code)
    total += total_cost * int(code[0:3])

print(total)