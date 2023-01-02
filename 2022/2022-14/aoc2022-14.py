import os
from collections import defaultdict
from math import floor


def sim_sand(grid, point, max_y, add_floor):
    # check down, then down-left, then down-right
    # return True if sand stopped, false if it fell through the void
    if grid[point] == 'o':
        return False
    nx, ny = point
    while max_y > ny:
        dy = 1
        # down
        if grid[(nx, ny+dy)] == '.':
            nx, ny = (nx, ny+dy)
        # down-left
        elif grid[(nx-1, ny+dy)] == '.':
            nx, ny = (nx-1, ny+dy)
        # down-right
        elif grid[(nx+1, ny+dy)] == '.':
            nx, ny = (nx+1, ny+dy)
        # stopped
        else:
            grid[(nx, ny)] = 'o'
            return True
    return False


def build_grid(shapes, void):
    grid = defaultdict(lambda: '.')
    max_x, max_y = 0, 0
    min_x = float('inf')
    for shape in shapes:
        # add '#' between each point pair
        for (p0x, p0y), (p1x, p1y) in zip(shape, shape[1:]):
            max_y = max(max_y, p0y, p1y)
            max_x = max(max_x, p0x, p1x)
            min_x = min(min_x, p0x, p1x)
            xdist, ydist = (p1x-p0x), (p1y-p0y)
            if xdist:
                sign = 1
                if xdist < 0:
                    sign = -1
                for i in range(abs(xdist)+1):
                    grid[(p0x + (sign * i), p0y)] = '#'
            else:  # ydist
                sign = 1
                if ydist < 0:
                    sign = -1
                for i in range(abs(ydist)+1):
                    grid[(p0x, p0y + (sign * i))] = '#'
    # add a floor 2 blocks below
    if not void:
        max_y += 2
        for x in range(min_x-1000, max_x+1000):
            grid[(x, max_y)] = '#'

    return grid, max_y


def pretty_print(grid, top_left, lower_right):
    grid_str = ''
    tx, ty = top_left
    lx, ly = lower_right
    for y in range(ty, ly+1):
        row_str = ''
        for x in range(tx, lx+1):
            if (x == 500 and y == 0):
                row_str += '+'
            else:
                row_str += grid[(x, y)]
        grid_str += '%s\n' % row_str
    print(grid_str)


def get_points(shape):
    px = [point.split(',') for point in shape.split(' -> ')]
    points = [(int(p[0]), int(p[1])) for p in px]
    return points


#####
with open(os.getcwd() + '/2022-14/input.txt') as f:
    # 498,4 -> 498,6 -> 496,6 -> [complex(498,4), ...]
    shapes = [get_points(shape) for shape in f.read().splitlines()]

    # Part A
    grid, max_y = build_grid(shapes, void=True)
    count = 0
    while sim_sand(grid, (500, 0), max_y, add_floor=False):
        count += 1
    print('Part A: %i' % count)

    # Part B
    grid, max_y = build_grid(shapes, void=False)
    count = 0
    while sim_sand(grid, (500, 0), max_y, add_floor=True):
        count += 1
    print('Part B: %i' % count)
