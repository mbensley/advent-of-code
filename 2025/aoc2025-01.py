# Timings: Part A: XX:00 / Part B: XX:00
import os
from typing import TextIO

# https://docs.python.org/3/library/


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = True) -> list[str]:
    test_input = ['R11', 'L61', 'L1', 'R1']
    return test_input if test else f.read().splitlines()

def turn_dial(start: int, steps: int, direction: str) -> int:
    if direction == 'R':
        return (start+steps) % 100
    return (start-steps) % 100

with open(inputfile()) as f:
    input = getinput(f)

    num_zeros_a = 0
    num_zeros_b = 0
    cur = 50
    for l in input:
        dir = l[0]
        steps = int(l[1:])
        new_cur = turn_dial(cur, steps, dir)
        if new_cur == 0:
            num_zeros_a += 1
            num_zeros_b += 1
        num_zeros_b += (steps // 100)
        if dir == 'R' and new_cur < cur and new_cur != 0 and cur != 0:
            num_zeros_b += 1
        if dir == 'L' and new_cur > cur and new_cur != 0 and cur != 0:
            num_zeros_b += 1
        cur = new_cur

    print('Part A: %i' % num_zeros_a)
    print('Part B: %i' % num_zeros_b)
