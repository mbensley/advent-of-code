# Timings: Part A: 12:00 / Part B: 0:30
import os
from itertools import combinations

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read()

def get_empty_rows(input):
    ecols = []
    for i, line in enumerate(input.splitlines()):
        if all([c == '.' for c in line]):
            ecols.append(i)
    return ecols

def get_empty_cols(input):
    erows = []
    lines = input.splitlines()
    for j in range(len(lines[0])):
        found = False
        for line in lines:
            if line[j] != '.':
                found = True
        if not found:
            erows.append(j)
    return erows

def get_mdist(sx, sy, bx, by):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(sx-bx) + abs(sy-by)

with open(inputfile()) as f:
    PARTA = True
    input = getinput(f)
    galaxies = []
    GSYM = '#'
    expansion = 1 if PARTA  else 1000000 - 1
    ecols = get_empty_cols(input)
    erows = get_empty_rows(input)

    # Get the set of galaxy locations
    y, yo = 0, 0
    for line in input.splitlines():
        x, xo = 0, 0
        for c in line:
            if c == GSYM: galaxies.append((x+xo,y+yo))
            x += 1
            if x in ecols: xo += expansion
        y += 1
        if y in erows: yo += expansion
        
    # Calculate the total distance between all pairs
    total = 0
    for (x0,y0),(x1,y1) in combinations(galaxies, 2):
        total += get_mdist(x0,y0,x1,y1)

    print('Total Dist: %i' % total)
