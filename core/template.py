# Timings: Part A: 3:00 / Part B: 1:30
import os
from collections import defaultdict
from collections import deque
import heapq
import string
import queue
import ast
import re
from itertools import product
from itertools import combinations
from functools import cache
from math import floor
from copy import deepcopy


def inputfile():
    year_dir = '2015'
    filename = os.path.join(year_dir, 'input.txt')
    return os.path.join(os.getcwd(), filename)


def getinput(f, test):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read()


test = False
with open(inputfile()) as f:
    input = getinput(f, test)

    print('Part A: %i' % 0)
    print('Part B: %i' % 1)
