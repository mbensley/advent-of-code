# Timings: Part A: 9:00 / Part B: 02:15:00
import os
import sys

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def traverse(start, end, steps, dirmap):
    stepcount = 0
    curloc = start
    while curloc != end:
        next_step = steps[stepcount % len(steps)]
        curloc = dirmap[curloc][0] if next_step == 'L' else dirmap[curloc][1]
        stepcount += 1
    return stepcount

def computeGCD(x, y):
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if ((x % i == 0) and (y % i == 0)):
            gcd = i
    return gcd

def calcLCM(x,y):
    return (x*y) // computeGCD(x,y)

def be_a_ghost(start, end, steps, dirmap):
    curloc = [key for key in dirmap.keys() if key[-1] == start]
    # build the full list of visited locations given the input
    start2z = [] # from each start, look at all reachable Zs and calc the step differences
    for s_index, start_loc in enumerate(curloc):
        stepcount = 0
        d = {} # loc -> index -> (first, second stepcount)
        start2z.append(d)
        loc = start_loc
        while True:
            idx = stepcount % len(steps)
            next_step = steps[idx]
            loc = dirmap[loc][0] if next_step == 'L' else dirmap[loc][1]
            stepcount += 1
            if loc[-1] == end:
                if loc in d:
                    if len(d[loc]) == 2: break
                    d[loc].append(stepcount)
                else:
                    d[loc] = [stepcount]
                    start2z[s_index] = d
    # now, we have a start2z with all possible z locations and the delta for each cycle start time
    # It turns out for the input, len(d.keys()) == 1 so there's only ever 1 d range to check
    # Now, calculate the LCM of everything
    lcm = 1
    for d in start2z:
        min_lcm = sys.maxsize
        for y1,y2 in d.values():
            new_lcm = calcLCM(lcm,y2-y1)
            min_lcm = min(min_lcm, new_lcm)
        lcm = min_lcm
    return lcm

with open(inputfile()) as f:
    input = f.read().split('\n\n')
    steps = input[0]
    network = input[1].splitlines()

    dirmap = {}
    for line in network:
        key, t = line.split(' = ')
        l, r = t.replace('(', '').replace(')','').split(', ')
        dirmap[key] = (l,r)

    print('Part A: %i' % traverse('AAA', 'ZZZ', steps, dirmap))
    print('Part B: %i' % be_a_ghost('A', 'Z', steps, dirmap))
