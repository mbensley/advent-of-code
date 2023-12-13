# Timings: Part A: Untimed / Part B: XX:00
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

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read()

def diff(a,b):
    count = 0
    for x,y in zip(a,b):
        if x != y:
            count +=1
    return count

def check(grid, i, diff_budget):
    # symmetry is between i and i+1
    remaining_budget = diff_budget
    offset = i+1
    for j in range(i,-1,-1):
        d = diff(grid[j], grid[offset])
        if remaining_budget < d:
            return False
        remaining_budget -= d
        offset += 1
        if offset >= len(grid): break

    if remaining_budget == 0:
        #print("sym! at ", i, grid)
        return True

# return rows above
def get_hz(grid, diff_budget):
    for i, (a,b) in enumerate(zip(grid[::1], grid[1::1])):
        if diff(a,b) <= diff_budget and check(grid,i, diff_budget):
            return (i+1)
    return 0


def get_vt(grid, diff_budget, scale):
    # rotate right
    rgrid = []
    # for every column...
    for i in range(len(grid[0])):
        row = ''
        # ...walk up  every col
        for j in range(len(grid)-1,-1,-1):
            row += grid[j][i]
        rgrid.append(row)
    hz =  get_hz(rgrid, diff_budget)
    if hz:
        hz = scale*(hz)
    return hz

with open(inputfile()) as f:
    input = getinput(f)
    diff_budget = 1 # 0 for Part A, 1 for Part B
    grids = input.split('\n\n')
    grids = [[line for line in grid.splitlines()] for grid in grids]
    totala = 0
    for grid in grids:
        hz = 100*get_hz(grid, diff_budget)
        if hz: totala += hz
        else: totala += get_vt(grid, diff_budget, scale=1)

    print('Total: %i' % totala)
