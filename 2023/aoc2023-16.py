# Timings: Part A: 30:00 / Part B: 05:00
import os
from collections import defaultdict

EMPTY, FMIRROR, BMIRROR, VSPLIT, HSPLIT, EDGE = '.', '/', '\\', '|', '-', 'X'
UP, RIGHT, LEFT, DOWN = '^', '>', '<', 'v'

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input-s.txt')

def getinput(f, test=False):
    test_input = ['...']
    return test_input if test else f.read().splitlines()

def build_grid(input):
    grid = defaultdict(lambda: (EDGE,[]))
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            grid[(x,y)] = (c, []) # list of directions that have visited
    return grid

def count(grid):
    count = 0
    for c, vlist in grid.values():
        if c != EDGE and vlist:
            count += 1
    return count

def update_loc(loc, dir):
    delta = (0,0)
    if dir == UP:
        delta = (0,-1)
    if dir == DOWN:
        delta = (0,1)
    if dir == RIGHT:
        delta = (1,0)
    if dir == LEFT:
        delta = (-1,0)
    x,y = loc
    xx,yy = delta
    return (x+xx, y+yy)


def trace(grid, start, dir):
    nloc = start # (x,y)
    ndir = dir
    while True:
        c, vlist = grid[nloc] 
        if c == EDGE:
            return
        if dir in vlist:
            return
        
        # EMPTY, FMIRROR, BMIRROR, VSPLIT, HSPLIT, 
        vlist.append(dir)
        if c == EMPTY:
            nloc = update_loc(nloc, dir)
        elif c == FMIRROR: # /
            dirmap = {RIGHT: UP, LEFT: DOWN, UP: RIGHT, DOWN: LEFT}
            dir = dirmap[dir]
            nloc = update_loc(nloc, dir)
        elif c == BMIRROR: # \
            dirmap = {RIGHT: DOWN, LEFT: UP, UP: LEFT, DOWN: RIGHT}
            dir = dirmap[dir]
            nloc = update_loc(nloc, dir)
        elif c == VSPLIT: # |
            if dir in [UP, DOWN]:
                nloc = update_loc(nloc, dir)
            elif dir in [LEFT, RIGHT]:
                trace(grid, update_loc(nloc, UP), UP)
                trace(grid, update_loc(nloc, DOWN), DOWN)
                return
        elif c == HSPLIT: # -
            if dir in [LEFT, RIGHT]:
                nloc = update_loc(nloc, dir)
            elif dir in [UP, DOWN]:
                trace(grid, update_loc(nloc, RIGHT), RIGHT)
                trace(grid, update_loc(nloc, LEFT), LEFT)
                return

            
def grid_print(grid, maxx, maxy):
    out = ''
    for y in range(maxy):
        for x in range(maxx):
            c, vlist = grid[(x,y)]
            if vlist:
                c = '#'
            out += c
        out += '\n'
    print(out)


with open(inputfile()) as f:
    input = getinput(f)

    # Part A
    grid = build_grid(input)
    trace(grid, (0,0), RIGHT)

    print('Part A: %i' % count(grid))

    # Part B: try all the starting configurations
    max_score = 0
    for x in range(len(input[0])):
        # top row down
        grid = build_grid(input)
        trace(grid, (x,0), DOWN)
        max_score = max(max_score, count(grid))
        # bottom up
        grid = build_grid(input)
        trace(grid, (x, len(input)), UP)
        max_score = max(max_score, count(grid))
    for y in range(len(input)):
        # L to R
        grid = build_grid(input)
        trace(grid, (0,y), RIGHT)
        max_score = max(max_score, count(grid))
        # R to L
        grid = build_grid(input)
        trace(grid, (len(input[0]), y), LEFT)
        max_score = max(max_score, count(grid))
    print('Part B: %i' % max_score)
