import os
from collections import defaultdict
from collections import deque

delta_map = {'N': complex(0, -1),
             'NE': complex(1, -1),
             'NW': complex(-1, -1),
             'S': complex(0, 1),
             'SE': complex(1, 1),
             'SW': complex(-1, 1),
             'W': complex(-1, 0),
             'E': complex(1, 0)}


def pretty_print(grid: defaultdict, min_point: complex, max_point: complex):
    output = ''

    for y in range(int(min_point.imag), int(max_point.imag)+1):
        for x in range(int(min_point.real), int(max_point.real)+1):
            output += grid[complex(x, y)]
        output += '\n'
    print(output)


def get_bounds(grid: defaultdict) -> complex:
    min_point = complex(min(c.real for c in grid.keys()),
                        min(c.imag for c in grid.keys()))
    max_point = complex(max(c.real for c in grid.keys()),
                        max(c.imag for c in grid.keys()))
    poi_list = get_pois(grid, min_point, max_point, poi='#')
    min_point = complex(min(e.real for e in poi_list),
                        min(e.imag for e in poi_list))
    max_point = complex(max(e.real for e in poi_list),
                        max(e.imag for e in poi_list))
    return min_point, max_point


def get_pois(grid: defaultdict, min_point: complex, max_point: complex, poi: str) -> list:
    elf_list = []
    for x in range(int(min_point.real), int(max_point.real)+1):
        for y in range(int(min_point.imag), int(max_point.imag)+1):
            point = complex(x, y)
            if grid[point] == poi:
                elf_list.append(point)
    return elf_list


def check_dir(elf: complex, direction: str, grid: defaultdict) -> bool:
    # returns true if clear in direction: 'NSWEA'
    def is_empty(point: complex, ds: list):
        for d in ds:
            if grid[point+delta_map[d]] == '#':
                return False
        return True

    if direction == 'A':
        return is_empty(elf, list(delta_map.keys()))
    if direction == 'N':
        return is_empty(elf, ['N', 'NE', 'NW'])
    if direction == 'S':
        return is_empty(elf, ['S', 'SE', 'SW'])
    if direction == 'W':
        return is_empty(elf, ['W', 'NW', 'SW'])
    if direction == 'E':
        return is_empty(elf, ['E', 'NE', 'SE'])
    raise


test = False
filename = '/2022-23/input-t.txt' if test else '/2022-23/input.txt'
with open(os.getcwd() + filename) as f:
    grid = defaultdict(lambda: '.')
    for y, row in enumerate(f.read().splitlines()):
        for x, c in enumerate(row):
            grid[complex(x, y)] = c
    pretty_print(grid, *get_bounds(grid))
    max_rounds = 100000

    proposal_q = deque('NSWE')
    for r in range(max_rounds):
        if r % 250 == 0:
            print('Round %i' % r)
        min_point, max_point = get_bounds(grid)
        moves_dict = {}
        count_dict = defaultdict(lambda: 0)
        elf_list = get_pois(grid, min_point, max_point, poi='#')
        for elf in elf_list:
            # H1
            if not check_dir(elf, 'A', grid):
                # H2: Proposals
                for direction in proposal_q:
                    if check_dir(elf, direction, grid):
                        moves_dict[elf] = elf+delta_map[direction]
                        count_dict[elf+delta_map[direction]] += 1
                        break
        # H2: Moves
        for elf, move in moves_dict.items():
            if count_dict[move] == 1:
                grid[elf] = '.'
                grid[move] = '#'
        proposal_q.rotate(-1)
        if not count_dict.values() or min(count_dict.values()) > 1:
            print('Part B: Nothing moved in round: %i' % (r+1))
            break

    min_point, max_point = get_bounds(grid)
    # pretty_print(grid, min_point, max_point)
    print('Part A: %i' % len(get_pois(grid, min_point, max_point, poi='.')))
