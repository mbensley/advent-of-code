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

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['1-3 a: abcde']
    return test_input if test else f.read().splitlines()


with open(inputfile()) as f:
    input = getinput(f)

    totala, totalb = 0, 0
    for line in input:
        policy, password = line.split(': ')
        r, letter = policy.split(' ')
        lr, rr = r.split('-')
        # A
        c = password.count(letter)
        if c >= int(lr) and c <=int(rr):
            totala +=1
        # B
        x, y = password[int(lr)-1] == letter, password[int(rr)-1] == letter
        if (x and not y) or (not x and y):
            totalb += 1

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
