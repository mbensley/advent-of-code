# Timings: Part A: 5:30 / Part B: 7:00
from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53']
    return test_input if test else f.read().splitlines()


with open(inputfile()) as f:
    input = getinput(f)
    totala = 0
    ctmap = defaultdict(int)
    for line in input:
        gid, nums = line.split(': ')
        id = int(gid.split()[1])
        w, a = nums.split(' | ')
        wlist = w.split()
        alist = a.split()
        ctmap[id] += 1
        count = 0
        for aa in alist:
            if aa in wlist:
                count += 1
        for i in range(1,count+1):
            ctmap[id+i] += ctmap[id]
        if count:
            # 0,1,2,4,8,16,32,64
            totala += 2**(count-1)
    totalb = sum(ctmap.values())

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
