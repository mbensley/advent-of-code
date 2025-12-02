# Timings: Part A: XX:00 / Part B: XX:00
import os
from typing import TextIO

# https://docs.python.org/3/library/

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = True) -> list[str]:
    test_input = ['11-22,95-115'] # A: 132, B: 243
    return test_input if test else f.read().splitlines()

def get_num_repeats(min_val: int, max_val: int) -> int:
    id_sum = 0
    for next_val in range(min_val, max_val+1):
        vstr = str(next_val)
        if len(vstr) % 2 != 0: continue
        if vstr[:len(vstr)//2] == vstr[len(vstr)//2:]:
            id_sum += next_val
    return id_sum

def get_num_repeats_b(min_val: int, max_val: int) -> int:
    id_sum = 0
    for next_val in range(min_val, max_val+1):
        vstr = str(next_val)
        # get all the divisors of len(vstr)
        # for each divisor, check if each slice of vstr is equal
        # if it is, add next_val to id_sum and continue
        vlen = len(vstr)
        for d in range(1, vlen // 2 + 1):
            if vlen % d == 0 and vstr[:d] * (vlen // d) == vstr:
                id_sum += next_val
                break
    return id_sum

with open(inputfile()) as f:
    input = getinput(f)[0]
    ranges = [x.split('-') for x in input.split(',')]
    pw_sum_a, pw_sum_b = 0, 0
    for l,r in ranges:
        pw_sum_a += get_num_repeats(int(l),int(r))
        pw_sum_b += get_num_repeats_b(int(l),int(r))

    print('Part A: %i' % pw_sum_a)
    print('Part B: %i' % pw_sum_b)
