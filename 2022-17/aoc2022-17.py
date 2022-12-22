import os
from collections import defaultdict
from math import floor

INITIAL_BUFFER = 3
L_BUFFER = 2
CHAMBER_WIDTH = 7


def get_dirs(dirlist: str):
    while True:
        for char in dirlist:
            yield char


def get_shapes(shapes: list):
    while True:
        for shape in shapes:
            yield shape


def construct_shapes() -> list:
    # points are in L, M, R column order so max_x always in ()[-1][0]
    line = ((0, 0), (1, 0), (2, 0), (3, 0))
    plus = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))
    bend = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
    vline = ((0, 0), (0, 1), (0, 2), (0, 3))
    box = ((0, 0), (1, 0), (0, 1), (1, 1))
    return [line, plus, bend, vline, box]


def check_points(shape: tuple, grid: dict, delta_x: int, delta_y: int) -> bool:
    for point in shape:
        px, py = point
        tx = px + delta_x
        ty = py + delta_y
        if grid[(tx, ty)] == '#' or ty < 0 or tx < 0 or tx > (CHAMBER_WIDTH-1):
            return False
    return True


def sim_rock(shape: tuple, start_y: int, dirs: iter, grid: dict, dir_count: int, debug) -> int:
    # starting location is points + (L_BUFFER, start_y)
    # iterate until we hit something then return max(start_y and the max_y of any point in our shape)
    points = shape[:]
    last_y = max(y for _, y in points)
    delta_x = L_BUFFER
    delta_y = start_y
    if debug:
        print('adding shape %s' % str(points))
    while True:
        # dir change
        dir_count += 1
        if debug:
            print('dx: %i, dy: %i' % (delta_x, delta_y))
        match next(dirs):
            case '<':
                # check walls and running into things
                if check_points(points, grid, delta_x-1, delta_y):
                    delta_x -= 1
            case '>':
                if check_points(points, grid, delta_x+1, delta_y):
                    delta_x += 1
        # down
        if check_points(points, grid, delta_x, delta_y-1):
            delta_y -= 1
        else:
            for px, py in points:
                tx, ty = px + delta_x, py+delta_y
                grid[(tx, ty)] = '#'
            if debug:
                print('highest y: %i' % (last_y+delta_y+1))
            return max(start_y - INITIAL_BUFFER, last_y + delta_y + 1), dir_count


def simulate(total_rocks: int, shape_list: list, dir_list: list, debug) -> int:
    dir_list = dir_list
    dirs = get_dirs(dir_list)
    grid = defaultdict(lambda: '.')
    shapes = get_shapes(shape_list)

    last_y = 0
    tdir_count = 0
    repeats = {}
    # const = 1
    count = 0
    extra_y = 0
    while count < total_rocks:
        print('new total')
        print(total_rocks)
        if count > 2000:
            print(count)
        last_y, dir_count = sim_rock(next(shapes), last_y + INITIAL_BUFFER,
                                     dirs, grid, 0, debug)
        tdir_count += dir_count

        if extra_y == 0:
            # look for repeats
            # get last floor
            dir_place = tdir_count % len(dir_list)
            shape_place = count % len(shape_list)
            pstr = ''
            for fx in range(6):
                pstr += grid[(fx, last_y-1)]
            if pstr not in repeats:
                repeats[pstr] = {}
            if (dir_place, shape_place) in repeats[pstr]:
                ocount, olast_y = repeats[pstr][(dir_place, shape_place)]
                delta_y = (last_y-1) - olast_y
                print('found repeat: y = %i, y2 = %i, delta: %i, count %i, ocount %i' %
                      (olast_y, last_y-1, delta_y, count, ocount))
                # repeats every:
                r = count - ocount
                times_to_repeat = floor((total_rocks-count) / r)
                extra_y = delta_y*times_to_repeat
                print('repeat')
                print(times_to_repeat)
                total_rocks -= r*times_to_repeat
                print('calc total')
                print(total_rocks)
            # return

                print('zooming ahead to %i' % count)
                # while (last_y < total_rocks - delta_y):
                #    last_y += delta_y
            else:
                repeats[pstr][(dir_place, shape_place)] = (count, last_y-1)
        count += 1

    return last_y + extra_y


with open(os.getcwd() + '/2022-17/input.txt') as f:
    part_a_rock_count = 2022  # real input ans: 3202, test input ans: 3068
    part_b_rock_count = 1000000000000  # test input ans: 1514285714288

    # fast simulation: there's some starting configuration with a bumpy floor and it will repeat
    # every N iterations, so just calculate how much the height grows when you cycle back
    # also have to make sure we're in the same location of the dir and shape iterators

    print('Part B: %i' % (simulate(part_b_rock_count,
                                   construct_shapes(), f.read().strip(), debug=False)))
