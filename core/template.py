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

test = True
no_file = False
filename = 'X/input.txt' if test else 'X/input-X.txt'
test_input = []
with open(os.getcwd() + '/advent-of-code/' + filename) as f:
    input = test_input if test and no_file else f.read().splitlines()

    print('Part A: %i' % 0)
    print('Part B: %i' % 1)
