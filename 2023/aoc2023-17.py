# Timings: Fun Run
from heapq import heappush, heappop
import os
import sys

UP, RIGHT, LEFT, DOWN = '^', '>', '<', 'v'

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input-s.txt')

def getinput(f, test=False):
    test_input = ['2111', '9924']
    return test_input if test else f.read().splitlines()

def build_grid(input):
    grid = {}
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            grid[(x,y)] = int(c)
    return grid, len(input[0]), len(input)

def dijkstra(grid, start_point, end_point, min_dist, max_dist):
    def get_new_dir(p, d):
        if d in (UP, DOWN): return (LEFT, RIGHT)
        return (UP, DOWN)

    visited = {} # (point, dir): cost
    point_q = []
    initial_cost = 0
    for dir in (UP, DOWN, LEFT, RIGHT):
        heappush(point_q, (initial_cost, start_point, dir))
    while point_q:
        cost, point, pdir = heappop(point_q)
        if (point, pdir) in visited and visited[(point, pdir)] <= cost:
           continue
        if point == end_point: return cost
        visited[(point, pdir)] = cost
        for newdir in get_new_dir(point, pdir):
            new_point = point
            new_cost = cost
            for icap in range(max_dist):
                new_point = update_loc(new_point, newdir)
                if new_point not in grid: break
                new_cost += grid[new_point]
                if icap+1 >= min_dist:
                    heappush(point_q, (new_cost, new_point, newdir))
    raise # No solution :(

def update_loc(loc, dir):
    dmap = {UP: (0,-1), DOWN: (0,1), RIGHT: (1,0), LEFT: (-1,0)}
    x,y = loc
    xx,yy = dmap[dir]
    return (x+xx, y+yy)

with open(inputfile()) as f:
    input = getinput(f)
    grid, maxx, maxy = build_grid(input)
    print('Part A: %i' % dijkstra(grid, (0,0), (maxx-1, maxy-1), min_dist=1, max_dist=3))
    print('Part B: %i' % dijkstra(grid, (0,0), (maxx-1, maxy-1), min_dist=4, max_dist=10))
