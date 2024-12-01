from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')


def getinput(f, test):
    test_input = [
        '3   4',
        '4   3',
        '2   5',
        '1   3',
        '3   9',
        '3   3']
    return test_input if test else f.read().splitlines()

def parta(input):
    totala = 0
    left_list, right_list = [], []
    for line in input:
        l,r = line.split()
        left_list.append(int(l))
        right_list.append(int(r))
    left_list.sort()
    right_list.sort()
    for idx, l in enumerate(left_list):
        r = right_list[idx]
        totala += abs(l-r)
    return totala

def partb(input):
    totalb = 0
    left_list, right_map = [], defaultdict(int)
    for line in input:
        l,r = line.split()
        left_list.append(int(l))
        right_map[int(r)] += 1
    for l in left_list:
        totalb += l * right_map[l]
    return totalb

test = False
with open(inputfile()) as f:
    input = getinput(f, test)

    print('Part A: %i' % parta(input))
    print('Part B: %i' % partb(input))
