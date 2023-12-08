# Timings: Part A: 10:00 / Part B: 1:00
from collections import defaultdict

def get_inputs():
    return [()]

def getways(time, dist):
    distmap = defaultdict(int)
    distcount = 0
    for speed in range(time+1):
        rtime = time - speed
        ndist = speed*rtime
        if ndist > dist:
            distcount += 1
    return distcount

total = 1
for time,dist in get_inputs():
    total *= getways(time, dist)
print('Part A/B: %i' % total)
