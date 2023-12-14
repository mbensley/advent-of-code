# Timings: Part A: 10:00 / Part B: 1h+
from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['']
    return test_input if test else f.read().splitlines()

def score_sym_tilt(grid, cols, rows):
    # Assumes everything has been tilted North
    total_score = 0
    for col in range(cols):
        score = 0
        next_score = rows
        for row in range(rows):
            c = grid[(row,col)]
            if c == '.': continue
            if c == 'O':
                score += next_score
                next_score -= 1
            if c == '#': next_score = rows - row - 1
        total_score += score
    return total_score

def score_in_place(grid, cols, rows):
    total_score = 0
    for r in range(rows):
        for c in range(cols):
            if grid[(r,c)] == 'O':
                total_score += rows - r
    return total_score

def prettyprint(grid, rows, cols):
    out = ''
    for row in range(rows):
        for col  in range(cols):
            out += grid[(row,col)]
        out += '\n'
    print(out)

def rotate(grid, cols, rows):
    rgrid = defaultdict(lambda: '.')
    # for every column...
    for col in range(cols):
        # ...walk up every row
        for row in range(rows-1,-1,-1):
            rgrid[(col, rows-1-row )] = grid[(row, col)]
    return rgrid

def spin(grid, cols, rows):
    # Tilt everything "North" but rotate through
    # all 4 directions (N, W, S, E)
    valid_locations = []
    for _ in range(4):
        for col in range(cols):
            valid_locations = []
            for row in range(rows):
                c = grid[(row,col)]
                if c in '.':
                    valid_locations.append(row)
                if c == 'O':
                    if valid_locations:
                        new_loc = valid_locations.pop(0)
                        grid[(new_loc,col)] = 'O'
                        if row != new_loc:
                            grid[(row,col)] = '.'
                            valid_locations.append(row)
                if c == '#':
                    valid_locations = []
        grid = rotate(grid, cols, rows)
        # Assume cols == rows otherwise add "cols, rows = rows, cols"
    return grid

def grid_hash(grid, cols, rows):
    out = ''
    for r in range(rows):
        for c in range(cols):
            out += grid[(r,c)]
        out += '\n'
    return out

# look for cycles in the spin pattern to skip ahead quickly
def multispin(grid, cycles, cols, rows):
    seen = {grid_hash(grid, cols, rows): 0}
    ngrid = grid
    cycle_count = 0
    while True:
        ngrid = spin(ngrid, cols, rows)
        cycle_count += 1
        if cycle_count >= cycles:
            return ngrid
        h = grid_hash(ngrid, cols, rows)
        if h in seen:
            cycle_dist = cycle_count - seen[h]
            if cycle_dist == 0:
                return ngrid
            cycle_count = cycles - ((cycles-cycle_count) % cycle_dist)
        else:
            seen[h] = cycle_count

with open(inputfile()) as f:
    input = getinput(f)
    grid = defaultdict(lambda: '.')
    for row, line in enumerate(input):
        for col, c in enumerate(line):
            grid[(row,col)] = c
    cols, rows = len(input[0]), len(input)
    
    print('Part A: %i' % score_sym_tilt(grid, cols, rows))
    print('Part B: %i' % score_in_place(multispin(grid, 1000000000, cols, rows), cols, rows))
