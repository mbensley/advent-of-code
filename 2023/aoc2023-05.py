# Timings: Untimed, a million billion years
import os
import math
import sys

def get_seed_list(seeds):
    return list(zip(seeds[::2], seeds[1::2]))

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().split('\n\n')

def convert(m, value):
    def contained(start, l, v):
        return v >= start and v <= (start + l)

    for line in m:
        dest_s, source_s, length = line
        if contained(int(source_s), int(length), value):
            offset = int(dest_s) - int(source_s)
            return offset + value
    return value

def seed2location(seed, maps):
    v = seed
    for idx, m in enumerate(maps):
        v = convert(m, v)
    return v

def parse_input(input):
    def build(lines):
        ret = []
        for line in lines:
            a,b,c = line.split()
            ret.append((int(a), int(b), int(c)))
        ret.sort(key=lambda x: x[1])
        return ret
    
    seeds = [int(e) for e in input.pop(0).split(': ')[1].split()] # seeds: x x x
    maps = [build(e.split('\n')[1:]) for e in input]
    return seeds, maps

def unconvert(m, value):
    def contained(start, l, v):
        return v >= start and v <= (start + l)

    for line in m:
        dest_s, source_s, length = line
        if contained(int(dest_s), int(length), value):
            offset = int(source_s) - int(dest_s)
            return offset + value
    return value

def location2seed(loc, maps):
    v = loc
    for idx, m in enumerate(maps):
        v = unconvert(m, v)
    return v


def checkvalidseed(seed, seedlist):
    for start, r in seedlist:
        if seed >= start and seed <= (start+r):
            return True
    return False

with open(inputfile()) as f:
    input = getinput(f)
    seeds, conversion_maps = parse_input(input)
    
    # Part A
    min_loc = math.inf
    for seed in seeds:
        loc = seed2location(seed, conversion_maps)
        if loc < min_loc:
            min_loc = loc
    print('Part A: %i' % min_loc)

    # Part B: reverse map from
    print('Starting Part B (slow)')
    seed_list = get_seed_list(seeds)
    sensible_minimum = 0 # set this near the real answer for your input to run quickly!
    for loc in range(sensible_minimum, sys.maxsize):
        if loc % 250000 == 0: # Watch progress slowly!
            print('>', loc)
        seed = location2seed(loc, reversed(conversion_maps))
        if checkvalidseed(seed, seed_list):
            print('Part B: %i' % loc)
            break