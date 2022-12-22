# input: all the items in each rucksack
# rucksacks have 2 compartments
# items are single lower or uppercase letter
# first half are first compartment, etc
# items have priority a-z = 1 - 26 A-Z = 27-52
import string
import os


def get_input_test():
    return [
        'vJrwpWtwJgWrhcsFMMfFFhFp', 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
        'PmmdzqPrVvPwwTWBwg', 'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 'ttgJtRGJQctTZtZT',
        'CrZsJsPPZsGzwwsLwLmpwMDw'
    ]


def find_common_item(sack):
    compartment_size = int(len(sack) / 2)
    compartment_a = set(sack[0:compartment_size])
    compartment_b = set(sack[compartment_size:])
    return compartment_a.intersection(compartment_b).pop()


def get_priority(item):
    return (string.ascii_lowercase + string.ascii_uppercase).index(item) + 1


with open(os.getcwd() + '/2022-03/input.txt') as f:
    input = [x for x in f.read().splitlines()]
    print('Part A: %i' % sum(map(get_priority, map(find_common_item, input))))

    # part B
    priority_sum = 0
    sack_list = input
    while sack_list:
        s0 = set(sack_list.pop())
        s1 = set(sack_list.pop())
        s2 = set(sack_list.pop())
        common_item = s0.intersection(s1).intersection(s2).pop()
        priority_sum += get_priority(common_item)
    print('Part B: %i' % priority_sum)
