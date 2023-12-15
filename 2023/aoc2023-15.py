# Timings: Part A: 2:30 / Part B: 20:00
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = 'HASH'
    return test_input if test else f.read()

def aochash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = h % 256
    return h

def calc_power(boxes):
    power = 0
    for bid, box in enumerate(boxes):
        for slot, (_, fl) in enumerate(box):
            power += (bid+1)*(slot+1)*int(fl)
    return power

def configure(input):
    def contains_label(box, label):
        for i, (bl, fl) in enumerate(box):
            if label == bl:
                return True, i
        return False, 0

    boxes = [[] for _ in range(256)]
    for s in input.split(','):
        if '=' in s:
            label, fl = s.split('=')
            boxid = aochash(label)
            contains, bid = contains_label(boxes[boxid], label)
            if contains:
                boxes[boxid][bid] = (label, fl)
            else:
                boxes[boxid].append((label, fl))
        if '-' in s:
            label = s[:-1]
            boxid = aochash(label)
            contains, bid = contains_label(boxes[boxid], label)
            if contains:
                boxes[boxid].pop(bid)
    return boxes

with open(inputfile()) as f:
    input = getinput(f)

    print('Part A: %i' % sum(aochash(s) for s in input.split(',')))
    print('Part B: %i' % calc_power(configure(input)))
