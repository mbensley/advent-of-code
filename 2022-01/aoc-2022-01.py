import os
import heapq


with open(os.getcwd() + '/2022-01/input.txt') as f:
    cal_list = []
    for pack in f.read().split('\n\n'):
        cal_list.append(sum([int(item) for item in pack.split('\n')]))
    cal_list.sort()

    print('Part A: %i' % sum(cal_list[-1:]))
    print('Part B: %i' % sum(cal_list[-3:]))

    print('Part A: %i' % heapq.nlargest(1, cal_list).pop())
    print('Part B: %i' % sum(heapq.nlargest(3, cal_list)))
