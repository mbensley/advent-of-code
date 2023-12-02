# Timings: Part A: 3:44 / Part B: 30:00
import os


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')


def getinput(f, test):
    test_input = ['1xxx',
                  'xxx3',
                  'two1nine',
                  'eightwothree',
                  'abcone2threexyz',
                  'xtwone3four',
                  '4nineeightseven2',
                  'zoneight234',
                  '7pqrstsixteen']
    return test_input if test else f.read().splitlines()


def getnums():
    return ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def getfirstdigit(line):
    for idx, c in enumerate(line):
        if c.isdigit():
            return idx, int(c)
    return None


def getfirstnum(line):
    # This will fail if there are no digits in your string!
    firstdigit_idx, firstdigit = getfirstdigit(line)
    sidx = len(line) + 1
    # Look for a number word and get the lowest index
    sfirstdigit = None
    for idx, num in enumerate(getnums()):
        i = line.find(num)
        if i > -1 and i < sidx:
            sidx = i
            sfirstdigit = idx + 1
    if sidx < firstdigit_idx:
        return sfirstdigit
    return firstdigit


def getlastnum(line):
    # This will fail if there are no digits in your string!
    lastdigit_idx, lastdigit = getfirstdigit(reversed(line))
    lastdigit_idx = len(line) - lastdigit_idx - 1
    # Look for a number word and get the highest index
    sidx = -1
    slastdigit = None
    for idx, num in enumerate(getnums()):
        i = line.rfind(num)
        if i > -1 and i > sidx:
            sidx = i
            slastdigit = idx+1
    if sidx > lastdigit_idx:
        return slastdigit
    return lastdigit


test = False
with open(inputfile()) as f:
    input = getinput(f, test)

    totala, totalb = 0, 0
    for line in input:
        totala += (getfirstdigit(line)[1] * 10) + \
            getfirstdigit(reversed(line))[1]
        totalb += (getfirstnum(line) * 10) + getlastnum(line)
    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
