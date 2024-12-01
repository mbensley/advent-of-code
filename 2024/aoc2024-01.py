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

def calc_similarity_a(input):
    total_delta = 0
    left_list, right_list = [], []
    for line in input:
        l, r = line.split()
        left_list.append(int(l))
        right_list.append(int(r))
    left_list.sort()
    right_list.sort()
    for idx, l in enumerate(left_list):
        total_delta += abs(l - right_list[idx])
    return total_delta

def calc_similarity_b(input):
    total_delta = 0
    left_list, right_map = [], defaultdict(int)
    for line in input:
        l, r = line.split()
        left_list.append(int(l))
        right_map[int(r)] += 1
    for l in left_list:
        total_delta += l * right_map[l]
    return total_delta

test = False
with open(inputfile()) as f:
    input = getinput(f, test)
    print('Part A: %i' % calc_similarity_a(input))
    print('Part B: %i' % calc_similarity_b(input))
