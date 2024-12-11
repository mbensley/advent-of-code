from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

def get_valid_moves(grid, start, height):
    valid_moves = []
    for dirx,diry in [(0, -1),(-1, 0),(1,0),(0, 1)]:
        startx,starty = start
        new_loc = (startx+dirx, starty+diry)
        if grid[new_loc] == height:
            valid_moves.append(new_loc)
    return valid_moves

def reachable(start, grid, target_height=9, calc_paths=False):
    cur_height = 0
    reachable = []
    pathQ = [(start, cur_height)]
    while pathQ:
        loc, height = pathQ.pop()
        valid_moves = get_valid_moves(grid, loc, height+1)
        if height+1 == target_height:
            reachable.extend(valid_moves)
        else:
            for m in valid_moves:
                pathQ.append((m, height+1))
    if calc_paths:
        return len(reachable)
    return len(set(reachable))

OUT_OF_BOUNDS = '#'
with open(inputfile()) as f:
    input = getinput(f)
    trailheads = []
    grid = defaultdict(lambda: OUT_OF_BOUNDS)
    for y, line in enumerate(input):
        for x, v in enumerate(line):
            v = int(v)
            if v == 0:
                trailheads.append((x,y))
            grid[(x,y)] = v
    
    totala, totalb = 0, 0
    for start in trailheads:
        a=reachable(start, grid, calc_paths=False)
        b=reachable(start, grid, calc_paths=True)
        totala += a
        totalb += b

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
