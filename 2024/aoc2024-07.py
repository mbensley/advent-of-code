import os
from itertools import product


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=True):
    test_input = [
        '190: 10 19',
        '3267: 81 40 27',
        '83: 17 5',
        '156: 15 6',
        '7290: 6 8 6 15',
        '161011: 16 10 13',
        '192: 17 8 14',
        '21037: 9 7 18 13',
        '292: 11 6 16 20'
    ]
    return test_input if test else f.read().splitlines()

SUM, MULT, CAT = '+', '*', '|'
def has_valid_solution(total, operands, oplist):
    def calc(operand_list, operator_list):
        while len(operator_list) > 0:
            a = operand_list.pop(0)
            b = operand_list.pop(0)
            operator = operator_list.pop()
            if operator == SUM:
                operand_list.insert(0, a+b)
            if operator == MULT:
                operand_list.insert(0, a*b)
            if operator == CAT:
                operand_list.insert(0, int(str(a) + str(b)))
        return operand_list.pop()
    operand_list = [int(x) for x in operands.split()]
    # generate combinations of len(op_list) - 1 operations then execute them
    combinations = product(oplist, repeat=len(operand_list)-1)
    for operator_list in combinations:
        c = calc(operand_list.copy(), list(operator_list))
        if  c == total:
            return True
    return False

with open(inputfile()) as f:
    input = getinput(f)

    totala, totalb = 0, 0
    for line in input:
        total, operands = line.split(': ')
        total = int(total)
        if has_valid_solution(total, operands, '+*'):
            totala += total
        if has_valid_solution(total, operands, '+*|'):
            totalb += total

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
