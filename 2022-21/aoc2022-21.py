import os
import re
from math import floor


def solve(target, symbols):
    tval = symbols[target]
    if isinstance(tval, int):
        return int(tval)
    a, o, b = tval
    match o:
        case '+':
            return solve(a, symbols) + solve(b, symbols)
        case '-':
            return solve(a, symbols) - solve(b, symbols)
        case '*':
            return solve(a, symbols) * solve(b, symbols)
        case '/':
            return solve(a, symbols) / solve(b, symbols)
        case '=':
            return solve(a, symbols), solve(b, symbols)
        case _:
            raise Exception('didnt find operator: %s' % o)


with open(os.getcwd() + '/2022-21/input.txt') as f:
    lines = [line.split(': ') for line in f.read().splitlines()]
    # process numbers
    symbols = {}
    part_b = True
    for name, job in lines:
        nlist = re.findall(r'(\d+)', job)
        if len(nlist) > 0:  # job is a number
            symbols[name] = int(nlist[0])
        else:  # job is a function
            expr = job.split(' ')
            if name == 'root' and part_b:
                expr[1] = '='
            symbols[name] = [expr[0], expr[1], expr[2]]
    symbols['humn'] = 0
    l, r = 0, 5279500000000
    # bsearch
    while True:
        a, b = solve('root', symbols)
        if a == b:
            print('humn: %i' % symbols['humn'])
            break
        if a < b:
            r = symbols['humn']
            symbols['humn'] = floor((l+r)/2)
        if a > b:
            l = symbols['humn']
            symbols['humn'] = floor((l+r)/2)
