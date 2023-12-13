# Timings: Untimed
import os
import re
from functools import cache

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['.? 1']
    return test_input if test else f.read().splitlines()

@cache
def match(record, groups):
    # strip leading '.'s
    m = re.match(r'\.+', record)
    if m:
        return match(record[m.end():], groups)
    if not groups:
        if "#" in record: return 0
        return 1
    if not record:
        if groups: return 0
        return 1
    if record.count('?') == 0:
        subrecords = [r for r in record.split('.') if r]
        if len(subrecords) != len(groups): return 0
        for i in range(len(subrecords)):
            if len(subrecords[i]) != groups[i]: return 0
        return 1 # pass # validate the string, 1 if valid 0 if not

    # brute force, try everything!
    #lstr = record.replace('?', '#', 1)
    #rstr = record.replace('?', '.', 1)
    #return match(lstr, groups) + match(rstr, groups)

    # non-brute force: build a whole group at a time
    total = 0
    # Look for runs of # and ? that are next to a . ? or end the line
    m = re.match(r'[\?#]{%i}(\.|\?|$)' % groups[0], record)
    # Assume that the first ? is broken / lstr
    if m:
        total += match(record[m.end():], groups[1:])
    # Assume the first ? is working / rstr
    if re.match(r'\?', record):
        total += match(record[1:], groups)
    return total

   
with open(inputfile()) as f:
    input = getinput(f)

    totala = 0
    for line in input:
        record, g = line.split(' ')
        groups = tuple(int(i) for i in g.split(','))
        c = match(record, groups)
        totala += c
    print('Part A: %i' % totala)

    totalb = 0
    for line in input:
        record, g = line.split(' ')
        record = '?'.join([record for _ in range(5)])
        g = ','.join([g for _ in range(5)])
        groups = tuple(int(i) for i in g.split(','))
        c = match(record, groups)
        totalb += c
    print('Part B: %i' % totalb)
