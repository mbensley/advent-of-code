# Timings: Part A: 2:50 / Part B: 3:05
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

with open(inputfile()) as f:
    input = getinput(f)
    
    # Part A
    hz, vt = 0, 0
    for line in input:
        dir, x = line.split()
        x = int(x)
        if dir == 'forward':
            hz += x
        if dir == 'up':
            vt -= x
            if vt < 0:
                vt = 0
        if dir == 'down':
            vt += x
    totala = hz*vt

    # Part B
    hz, vt, aim = 0,0,0
    for line in input:
        dir, x = line.split()
        x = int(x)
        if dir == 'forward':
            hz += x
            vt += aim * x
            if vt < 0:
                vt = 0
        if dir == 'up':
            aim -= x
        if dir == 'down':
            aim += x
    totalb = hz*vt

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
