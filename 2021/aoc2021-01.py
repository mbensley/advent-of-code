# Timings: Part A: 3:00 / Part B: 1:30
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test):
    test_input = [199,
                  200,
                  208,
                  210,
                  200,
                  207,
                  240,
                  269,
                  260,
                  263]
    return test_input if test else f.read().splitlines()


test = False
with open(inputfile()) as f:
    input = getinput(f, test)
    last = -1
    counta = 0
    for depth in input:
        if int(depth) > last:
            counta += 1
        last = int(depth)

    dlist = [int(input[0]), int(input[1]), int(input[2])]
    input = input[2:]
    last = sum(dlist)
    countb = 0
    for c in input:
        dlist[2] = int(c)
        s = sum(dlist)
        if s > last:
            countb += 1
        last = s
        dlist = [dlist[1], dlist[2], 0]

    print('Part A: %i' % (counta-1))
    print('Part B: %i' % (countb))
