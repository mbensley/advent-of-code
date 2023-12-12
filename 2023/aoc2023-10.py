# Timings: Part A: 54:00 / Part B: Untimed
from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

def get_route_len(x, y, px, py, grid, start):
    dist = 0
    route = []
    route.append(start)
    cx,cy = x,y
    while grid[(cx,cy)] != start:
        cur_sym = grid[(cx,cy)]
        N = (cx,cy-1)
        S = (cx,cy+1)
        E = (cx+1,cy)
        W = (cx-1, cy)
        possible_next = []
        if cur_sym == '|':
            if (px,py) == S:
                possible_next = [N]
            else: possible_next = [S]
        if cur_sym == '-':
            if (px,py) == E:
                possible_next = [W]
            else: possible_next = [E]
        if cur_sym == 'L':
            if (px,py) == N:
                possible_next = [E]
            else: possible_next = [N]
        if cur_sym == 'J':
            if (px,py) == N:
                possible_next = [W]
            else: possible_next = [N]
        if cur_sym == '7':
            if (px,py) == S:
                possible_next = [W]
            else: possible_next = [S]
        if cur_sym == 'F':
            if (px,py) == S:
                possible_next = [E]
            else: possible_next = [S]
        if cur_sym == '.':
            possible_next = []
        # |, -, L, J, 7, F
        # now follow all possible routes
        if len(possible_next) == 0:
            break
        n = possible_next[0]
        dist += 1
        px,py = cx,cy
        route.append((cx,cy))
        cx,cy = n
    return dist, route

with open(inputfile()) as f:
    input = getinput(f)

    # Build the grid
    grid = defaultdict(lambda: '.')
    start = (0,0)
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            grid[(x,y)] = c
            if c == 'S':
                start = (x,y)
    
    # Part A
    sx,sy = start
    # In my input, (sx, sy+1) is in the path
    # Could also infer what S is in start at (sx,sy)
    totala, route = get_route_len(sx, sy+1, sx, sy, grid, start)
    totala = (totala + 1) // 2
    
    # Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
    # Sum over all the points that make up the polygon/route
    sum = 0
    for i in range(len(route)):
        x1, y1 = route[i]
        x2, y2 = route[(i+1) % len(route)]
        sum += x1 * y2 - y1 * x2
    area = abs(sum / 2)
    totalb = 1 + area - len(route) / 2

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
