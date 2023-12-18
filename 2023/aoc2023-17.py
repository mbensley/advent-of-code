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

# https://docs.python.org/3/library/
UP, RIGHT, LEFT, DOWN = '^', '>', '<', 'v'


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input-s.txt')

def getinput(f, test=False):
    test_input = ['219', '914']
    return test_input if test else f.read().splitlines()

def build_grid(input):
    grid = defaultdict(lambda: '#')
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            grid[(x,y)] = int(c)
    return grid

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getxy(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '(%i,%i)' % (self.x, self.y)


class Vertex(object):

    def __init__(self, point, cost):
        self.cost = cost
        self.neighbors = set()
        self.point = point

    def __hash__(self):
        return hash(self.point)

    def __eq__(self, other):
        return self.point.x == other.point.x and self.point.y == other.point.y

    def __repr__(self):
        neighbor_pts = ['%s[%s]' % (v.point, v.cost) for v in self.neighbors]
        return '(%i,%i)[%s]{%s}' % (self.point.x, self.point.y, self.cost, str(neighbor_pts))
 
def djikstra(vdict, start_point, end_point, flood, cap):
    def find_in_queue(v, q):
      for _,u in q:
        if v == u:
          return True
      return False

    def unqueue(q, v, alt):
      for x, (_, element) in enumerate(q):
        if v == element:
          _,p = q.pop(x)
          q.append((alt, p))
          return
  
    cost_dict = {}
    point_q = []
    remaining_cap = cap
    cur_dir = None
 
    # point_q is the set of unvisited nodes
    for vertex in vdict.values():
      if vertex.point == start_point:
        cost_dict[vertex] = 0
        point_q.append((0, vertex))
      else:
        point_q.append((sys.maxsize, vertex))
        cost_dict[vertex] = sys.maxsize

    while point_q:
      point_q.sort(key=lambda x: x[0])
      p, u = point_q.pop(0)
      if p == sys.maxsize:
        return sys.maxsize, cost_dict
      for vertex in u.neighbors:
        # check for neighbors that we're allowed to reach due to the cap
        if vertex.point == end_point and not flood:
          return cost_dict[u] + vertex.cost, cost_dict
        if find_in_queue(vertex,point_q):
          alt = cost_dict[u] + vertex.cost
          if alt < cost_dict[vertex]:
            cost_dict[vertex] = alt
            unqueue(point_q, vertex, alt)
    return sys.maxsize, cost_dict

def get_vertex(dir, point, grid, vdict):
    np = Point(*update_loc(point.getxy(), dir))
    cost = grid[np.getxy()]
    if cost == '#': return None
    if np in vdict: return vdict[np]
    vdict[np] = Vertex(np, cost)
    return vdict[np]

def build_graph(grid, maxx, maxy):
    def connected(u, v):
        return u and v

    point = Point(0, 0)
    vdict = {point: Vertex(point, grid[point.getxy()])}
    # Node has a cost [1-9] and neighbors
    # Generate neighbors
    for y in range(maxy):
        for x in range(maxx):
            point = Point(x, y)
            u = vdict[point]
            for dir in (UP, RIGHT, LEFT, DOWN):
                v = get_vertex(dir, point, grid, vdict)
                if connected(u, v):
                    u.neighbors.add(v)
                if connected(v,u):
                    v.neighbors.add(u)
    return vdict
    
def grid_print(grid, maxx, maxy):
    out = ''
    for y in range(maxy):
        for x in range(maxx):
            out += grid[(x,y)]
        out += '\n'
    print(out)

def update_loc(loc, dir):
    dmap = {UP: (0,-1), DOWN: (0,1), RIGHT: (1,0), LEFT: (-1,0)}
    x,y = loc
    xx,yy = dmap[dir]
    return (x+xx, y+yy)

with open(inputfile()) as f:
    input = getinput(f)
    grid = build_grid(input)
    maxx, maxy = len(input[0]), len(input)
    vdict = build_graph(grid, maxx, maxy)
    min_cost, cd = djikstra(vdict, Point(0,0), Point(maxx-1, maxy-1), flood=False, cap=3)

    print('Part A: %i' % min_cost)
    print('Part B: %i' % 1)
