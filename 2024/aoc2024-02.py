import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = [
        '7 6 4 2 1',
        '1 2 7 8 9',
        '9 7 6 2 1',
        '1 3 2 4 5',
        '8 6 4 4 1',
        '1 3 6 7 9',
    ]
    return test_input if test else f.read().splitlines()

def is_safe(input_list, max_dist = 3):
    increasing = input_list[1] - input_list[0] > 0

    e0 = input_list[0]
    for e1 in input_list[1:]:
        if e0 == e1: return False
        if increasing:
            if (e1 > e0 + max_dist or e1 < e0):
                return False
        else:
            if e1 < e0 - max_dist or e1 > e0:
                return False
        e0 = e1
    return True

def is_safe_b(input_list):
    if is_safe(input_list): return True
    # Otherwise try removing elements!
    for idx in range(len(input_list)):
        if is_safe(input_list[:idx] + input_list[idx+1:]): return True
    return False

with open(inputfile()) as f:
    input = getinput(f)
    
    totala, totalb = 0, 0
    for line in input:
        input_list = [int(x) for x in line.split()]
        if is_safe(input_list):
            totala += 1
        if is_safe_b(input_list):
            totalb += 1

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
