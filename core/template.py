# Timings: Part A: XX:00 / Part B: XX:00
from collections import defaultdict
from collections import deque
import ast
import hashlib
import heapq
import math
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
from typing import TextIO

# https://docs.python.org/3/library/


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = False) -> list[str]:
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read().splitlines()


with open(inputfile()) as f:
    input = getinput(f)

    print('Part A: %i' % 0)
    print('Part B: %i' % 1)
