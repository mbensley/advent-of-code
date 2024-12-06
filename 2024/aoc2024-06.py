from collections import defaultdict
import os


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

OUT_OF_BOUNDS = 'x'
CRATE = '#'
START_TOKEN = '^'
EMPTY = '.'

delta_map = {'^': (0, -1), '<': (-1, 0), '>': (1,0), 'v': (0, 1)}
turn_map = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
# returns set() and is_cycle
def sim_guard(grid, start):
    def update(grid, cur_location, orientation):
        deltax, deltay = delta_map[orientation]
        cx,cy = cur_location
        next_location = (cx+deltax, cy+deltay)
        if grid[next_location] == CRATE:
            orientation = turn_map[orientation]
        else:
            cur_location = next_location
        return cur_location, orientation
    
    visited = set()
    orientation = '^'
    cur_location = start
    # Simulate movement until the gaurd leaves the grid or there's a cycle
    while grid[cur_location] != OUT_OF_BOUNDS:
        if (cur_location, orientation) in visited:
            return visited, True
        visited.add((cur_location, orientation))
        cur_location, orientation = update(grid, cur_location, orientation)
    return visited, False

def count_unique_locations(visited):
    return len(set(x for (x,y) in visited))

# Note: if you don't do this copy and modify the grid in place you can save ~5 seconds
def get_new_grid(grid, x, y):
    new_grid = grid.copy()
    new_grid[(x,y)] = CRATE
    return new_grid

def count_cycles(input, grid, start):
    cycle_count, try_count = 0, 0
    # Note: searching only reachable locations saves 80% of runtime (~25 seconds)
    reachable_locations = set(x for (x,y) in sim_guard(grid, start)[0])
    for x,y in reachable_locations:
        if grid[(x,y)] == EMPTY:
            try_count += 1
            new_grid = get_new_grid(grid, x, y)
            if sim_guard(new_grid, start)[1]:
                cycle_count += 1
            print('Cycle count: %i of %i' % (try_count, len(reachable_locations)), end='\r')
    print('                                 ', end='\r') # blank out the progress counter
    return cycle_count

with open(inputfile()) as f:
    input = getinput(f)
    grid = defaultdict(lambda: OUT_OF_BOUNDS)

    start = None
    for y, line in enumerate(input):
        for x, val in enumerate(line):
            grid[(x,y)] = val
            if val == START_TOKEN:
                start = (x,y)
                grid[start] = '.'
    
    print('Part A: %i' % count_unique_locations(sim_guard(grid, start)[0]))
    print('Part B: %i' % count_cycles(input, grid, start))
