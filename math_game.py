from random import randint


def create_math_games_params():
    operations = ["+","-","*"]
    numbers_in = []
    operations_in = []
    for _ in range(4):
        numbers_in.append(randint(1,100))

    while len(operations_in) < 3:
        ind = randint (0,2)
        operat = operations[ind]
        if operat == "*":
            if operat not in operations_in:
                operations_in.append(operations[ind])
        else:    
            operations_in.append(operations[ind])
    

    str_ope = ""
    str_ope += str(numbers_in[0])
    for i in range(3):
        str_ope += str(operations_in[i])
        str_ope += str(numbers_in[i+1])


    while True:
        try:
            ind = operations_in.index("*")
            operations_in.pop(ind)
            numbers_in[ind] = numbers_in[ind]*numbers_in[ind+1]
            numbers_in.pop(ind+1)
        except:
            break

    while True:
        if operations_in:
            op = operations_in.pop(0)
            if op == "+":
                numbers_in[0] = numbers_in[0] +  numbers_in[1]
            elif op == "-":
                numbers_in[0] = numbers_in[0] -  numbers_in[1]
            numbers_in.pop(1)
        else:
            break
    return(numbers_in[0],str_ope)        

