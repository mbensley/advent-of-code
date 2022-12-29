import string
import os


def find_common_item(sack):
    compartment_size = len(sack) // 2
    compartment_a = set(sack[0:compartment_size])
    compartment_b = set(sack[compartment_size:])
    return compartment_a.intersection(compartment_b).pop()


def get_priority(item):
    return (string.ascii_lowercase + string.ascii_uppercase).index(item) + 1


with open(os.getcwd() + '/2022-03/input-t.txt') as f:
    input = f.read().splitlines()
    print('Part A: %i' % sum(map(get_priority, map(find_common_item, input))))

    # Part B
    priority_sum = 0
    while input:
        s0 = set(input.pop())
        s1 = set(input.pop())
        s2 = set(input.pop())
        common_item = s0.intersection(s1).intersection(s2).pop()
        priority_sum += get_priority(common_item)
    print('Part B: %i' % priority_sum)
