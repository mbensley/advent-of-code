# Timings: Part A: XX:00 / Part B: XX:00
from collections import defaultdict
from collections import deque
import ast
import hashlib
from heapq import heappush, heappop
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
    return test_input if test else f.read().splitlines()


def build_grid_a(input):
    # get starting node and ending node
    x0, xN = None, None
    for x, tile in enumerate(input[0]):
        if tile == '.':
            x0 = x
    for x, tile in enumerate(input[1]):
        if tile == '.':
            xN = x
    
    grid = defaultdict()
    for y, line in enumerate(input):
        for x, tile in enumerate(line):
            grid[(x,y)] = tile
    
    grid_map = {}
    start_node = (x0, 0)
    end_node = (xN, len(input)-1)

    UP, RIGHT, LEFT, DOWN =  (0,-1),  (1,0), (-1,0), (0,1)
    nodeQ = queue.SimpleQueue()
    nodeQ.put(start_node)
    prev_pos = start_node
    while not nodeQ.empty():
        cur_node = nodeQ.get()
        cur_pos = cur_node
        dist_to_next_node = 0
        # check to see how many directions are possible from the current position
        valid_paths = []
        while len(valid_paths) <= 1:
            for dir in [UP, RIGHT, DOWN, LEFT]:
                next_pos = cur_pos + dir
                if cur_pos == start_node and dir == UP: continue # prevent out of bounds
                if next_pos == prev_pos: continue
                if grid[next_pos] == '.':
                    valid_paths.append(next_pos)
            if len(valid_paths == 1):
                dis_to_next_node += 1
                cur_pos = valid_paths.pop() # move to the only valid spot and keep iterating
            else: # we're at a branch
                # create new nodes
                pass



        prev_pos = cur_pos
    

    return grid_map, start_node, end_node


def grid_longest_path(grid_map, start_node, end_node):
    return 1

with open(inputfile()) as f:
    input = getinput(f)

    grid_map, start, end = build_grid_a(input)
    lengtha = grid_longest_path(grid_map, start, end)


    print('Part A: %i' % lengtha)
    print('Part B: %i' % 1)
