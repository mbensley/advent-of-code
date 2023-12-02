# Timings: Part A: 3:00 / Part B: 1:30
from collections import defaultdict
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
    year_dir = '2020'
    filename = os.path.join('advent-of-code', year_dir, 'input.txt')
    return os.path.join(os.getcwd(), filename)


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

    # print(input)
    print('Part A: %i' % (counta-1))
    print('Part B: %i' % (countb))
