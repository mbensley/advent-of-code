# Timings: Part A: 3:00 / Part B: 1:30
import os


def inputfile():
    year_dir = '2015'
    filename = os.path.join(year_dir, 'input.txt')
    return os.path.join(os.getcwd(), filename)


def getinput(f, test):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read()


with open(inputfile()) as f:
    oc, cc = 0, 0
    first_neg = float('inf')
    for i, c in enumerate(getinput(f, False)):
        if c == '(':
            oc += 1
        else:
            cc += 1
        if oc - cc == -1:
            first_neg = min(first_neg, i)
    print('Part A: %i' % (oc - cc))
    print('Part B: %i' % (first_neg+1))
