# Timings: Part A: 4:00 / Part B: 10:00
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['10 13 16 21 30 45','0 3 6 9 12 15']
    return test_input if test else f.read().splitlines()

def getnext(vals):
    seq = []
    for i in range(len(vals)-1):
        seq.append(vals[i+1] - vals[i])
    if any(seq):
        return getnext(seq) + vals[-1]
    return vals[-1]

def getprev(vals):
    seq = []
    for i in range(len(vals)-1):
        seq.append(-1*(vals[i+1] - vals[i]))
    if any(seq):
        x= vals[-1] - getprev(seq)
        return x
    return vals[-1]

with open(inputfile()) as f:
    input = getinput(f)
    totala, totalb = 0, 0
    for line in input:
        vals = [int(x) for x in line.split()]
        n = getnext(vals)
        nb = getprev(list(reversed(vals)))
        totala += n
        totalb += nb

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
