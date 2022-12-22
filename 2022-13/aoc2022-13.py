import os
import ast
import functools


def compare(l, r):
    # l and r are Packets: union[int, list]
    # both ints: lower int comes first, if equal check next element
    # both lists: compare list elements for high/low, don't need to be same length, if l runs out first, in same order
    # if one is an int, convert it to a list and retry
    # return -1 on l < r, 0 on equal, 1 on r > l
    if l == r:
        return 0
    match l, r:
        case int(), int():
            return -1 if l < r else 1
        case int(), list():
            return compare([l], r)
        case list(), int():
            return compare(l, [r])
    if l and r:
        comparison = compare(l[0], r[0])
        if comparison == 0:
            return compare(l[1:], r[1:])
        return comparison
    return 1 if l else -1


with open(os.getcwd() + '/2022-13/input.txt') as f:
    pair_list = [x.split('\n') for x in f.read().split('\n\n')]
    ans_list = [compare(ast.literal_eval(l), ast.literal_eval(r))
                for l, r in pair_list]

    sum = 0
    for index, ans in enumerate(ans_list):
        if ans == -1:
            sum += index+1
    print('Part A: %i' % sum)

    packet_list = [[[2]], [[6]]]
    for l, r in pair_list:
        packet_list.append(ast.literal_eval(l))
        packet_list.append(ast.literal_eval(r))
    packet_list.sort(key=functools.cmp_to_key(compare))
    i1 = packet_list.index([[2]]) + 1
    i2 = packet_list.index([[6]]) + 1
    print('Part B: %i' % (i1*i2))
