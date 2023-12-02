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
    target = 2020
    a = 0
    i_input = []
    for i in input:
        i_input.append(int(i))
    for v in input:
        i = int(v)
        if (target - i) in i_input:
            a = i * (target-i)
            break

    for i in i_input:
        ntarget = target - i
        ni_input = i_input.copy()
        ni_input.remove(i)
        for v in ni_input:
            if ntarget - v in ni_input:
                b = i * v * (ntarget-v)
                break

    print('Part A: %i' % (a))
    print('Part B: %i' % (b))
