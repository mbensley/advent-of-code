# #cals per item, one per line
# blank line in between each elf
# who has the most calories
import os


def count_top_n_calories(cal_list, top_n):
    total_cal_list = sorted([sum(elf_list) for elf_list in cal_list])
    return sum(total_cal_list[-top_n:])


def build_cal_list():
    with open(os.getcwd() + '/2022-01/input.txt') as f:
        cal_list = []
        for pack in f.read().split('\n\n'):
            cal_list.append([int(item) for item in pack.split('\n')])
        return cal_list


cal_list = build_cal_list()
print('Part A: %i' % count_top_n_calories(cal_list, 1))
print('Part B: %i' % count_top_n_calories(cal_list, 3))
