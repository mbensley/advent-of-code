import os


# is a completely in b or b completely in a
def is_range_contained(sa, ea, sb, eb):
    #   sa      ea
    #      sb eb
    return (sa <= sb and ea >= eb) or (sb <= sa and eb >= ea)


# does range_b overlap with range_a
def is_overlap(sa, ea, sb, eb):
    # either startA is in range of B or startB is in range of A
    return (eb >= sa >= sb) or (ea >= sb >= sa)


total_contained = 0
total_overlap = 0
with open(os.getcwd() + '/2022-04/input.txt', 'r') as f:
    lines = [line.split(',') for line in f.read().splitlines()]
    for range_a, range_b in lines:
        if is_range_contained(*map(int, range_a.split('-')), *map(int, range_b.split('-'))):
            total_contained += 1
        if is_overlap(*map(int, range_a.split('-')), *map(int, range_b.split('-'))):
            total_overlap += 1
print('Part A: %i' % total_contained)
print('Part B: %i' % total_overlap)
