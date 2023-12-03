from collections import defaultdict
import os
def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = [
        '467..114..',
        '...*......',
        '..35..633.',
        '......#...',
        '617*......',
        '5....+...5',
        '..592.....',
        '......755.',
        '...$.*....',
        '.664.598..']
    return test_input if test else f.read().splitlines()

def build_grid(lines):
    grid = defaultdict(lambda: '.')
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x,y)] = c
    return grid

def find_next_num(line, offset):
    x_start, x_end = 0,0
    in_num = False
    num_list = ''
    for x in range(offset, len(line)):
        x_end = x
        if in_num:
            if line[x].isdigit():
                num_list += line[x]
            else:
                break
        else:
            if not line[x].isdigit():
                continue
            x_start = x
            num_list += line[x]
            in_num = True
    if num_list == '':
        return -1, -1, None
    return x_start, x_end, int(num_list)


def find_adjacent_symbols(x_start, x_end, y, part_grid):
    def check_loc(x, y):
        return part_grid[(x, y)] != '.' and not part_grid[(x,y)].isdigit()

    for x in range(x_start, x_end):
        for xx,yy in [(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)]:
            if check_loc(xx,yy):
                return True
    return False

def find_adjacent_gear(x_start, x_end, y, part_grid, symbol='*'):
    def check_loc(x, y):
        return part_grid[(x,y)] == symbol
    for x in range(x_start, x_end):
        for xx,yy in [(x-1,y-1), (x-1,y), (x-1,y+1), (x,y-1), (x,y+1), (x+1,y-1), (x+1,y), (x+1,y+1)]:
            if check_loc(xx,yy):
                return (xx,yy)
    return None

with open(inputfile()) as f:
    input = getinput(f)

    part_grid = build_grid(input)
    maxx, maxy = len(input[0]), len(input)
    totala = 0
    for y, line in enumerate(input):
        x_start, x_end, num = find_next_num(line, 0)
        while num:
            if find_adjacent_symbols(x_start, x_end, y, part_grid):
                totala += num
            x_start, x_end, num = find_next_num(line, x_end+1)
    
    # Part B
    totalb = 0
    gear_map = defaultdict(list)
    for y, line in enumerate(input):
        x_start, x_end, num = find_next_num(line, 0)
        while num:
            loc = find_adjacent_gear(x_start, x_end, y, part_grid, symbol='*')
            if loc:
                gear_map[loc].append(num)
            x_start, x_end, num = find_next_num(line, x_end+1)
    for k,v in gear_map.items():
        if len(v) == 2:
            totalb += (v[0] * v[1])

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
