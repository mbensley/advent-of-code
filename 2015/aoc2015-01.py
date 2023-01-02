# Timings: Part A: 3:00 / Part B: 1:30
import os

filename = '/advent-of-code/2015/input.txt'
with open(os.getcwd() + filename) as f:
    oc, cc = 0, 0
    first_neg = float('inf')
    for i, c in enumerate(f.read()):
        if c == '(':
            oc += 1
        else:
            cc += 1
        if oc - cc == -1:
            first_neg = min(first_neg, i)
    print('Part A: %i' % (oc - cc))
    print('Part B: %i' % (first_neg+1))
