# Timings: Part A: 16:30 / Part B: 21:50
from collections import defaultdict
from collections import Counter
from collections import deque
import ast
import hashlib
import heapq
import os
import queue
import re
import string
import sys
from itertools import product
from itertools import combinations
from functools import cache
from math import floor
from copy import deepcopy

# https://docs.python.org/3/library/


def inputfile():
    year_dir = '2015'
    filename = os.path.join(year_dir, 'input.txt')
    return os.path.join(os.getcwd(), filename)


def getinput(f, test):
    test_input = ["turn on 887,9 through 959,629",
                  "turn off 539,243 through 559,965",
                  "toggle 831,394 through 904,860"]
    return test_input if test else f.read().splitlines()


def parse(line):
    lparts = line.split(' ')
    op = 't'
    aidx = 1
    bidx = 3
    a, b = None, None
    if lparts[0] == 'turn':
        op = lparts[1]
        aidx = 2
        bidx = 4
    aparts = lparts[aidx].split(',')
    a = complex(int(aparts[0]), int(aparts[1]))
    bparts = lparts[bidx].split(',')
    b = complex(int(bparts[0]), int(bparts[1]))
    return op, a, b


test = True
with open(inputfile()) as f:
    input = getinput(f, test)

    on_map = set()
    on_dict = defaultdict(int)
    part_a = False
    if part_a:
        for line in input:
            inst, pa, pb = parse(line)
            pax, pay = int(pa.real), int(pa.imag)
            pbx, pby = int(pb.real), int(pb.imag)
            if inst == 'on':
                for x in range(pax, pbx+1):
                    for y in range(pay, pby+1):
                        on_map.add(complex(x, y))
            if inst == 'off':
                for x in range(pax, pbx+1):
                    for y in range(pay, pby+1):
                        if complex(x, y) in on_map:
                            on_map.remove(complex(x, y))
            if inst == 't':
                for x in range(pax, pbx+1):
                    for y in range(pay, pby+1):
                        if complex(x, y) in on_map:
                            on_map.remove(complex(x, y))
                        else:
                            on_map.add(complex(x, y))
        print('Part A: %i' % len(on_map))
    else:
        for line in input:
            inst, pa, pb = parse(line)
            pax, pay = int(pa.real), int(pa.imag)
            pbx, pby = int(pb.real), int(pb.imag)
            if inst == 'on':
                for x in range(pax, pbx+1):
                    for y in range(pay, pby+1):
                        on_dict[complex(x, y)] += 1
            if inst == 'off':
                for x in range(pax, pbx+1):
                    for y in range(pay, pby+1):
                        if on_dict[complex(x, y)] > 0:
                            on_dict[complex(x, y)] = on_dict[complex(x, y)] - 1
            if inst == 't':
                for x in range(pax, pbx+1):
                    for y in range(pay, pby+1):
                        on_dict[complex(x, y)] += 2
        print('Part B: %i' % sum(on_dict.values()))
