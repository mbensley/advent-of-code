# Timings: Untimed but pretty long!
from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read().splitlines()

def grid_parse(input, parta):
    grid = defaultdict(lambda: '#') if parta else {}
    start = None
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            grid[(x,y)] = c
            if c == 'S':
                start = (x,y)
                grid[(x,y)] = '.'
    return grid, start

UP, RIGHT, LEFT, DOWN = '^', '>', '<', 'v'
def update_loc(loc, dir):
    x,y = loc
    xx,yy = {UP: (0,-1), DOWN: (0,1), LEFT: (-1,0), RIGHT: (1,0)}[dir]
    return (x+xx, y+yy)

def get_point(grid, x, y, maxx, maxy):
    def c(z, maxz):
        if z < 0: return (maxz - (abs(z) % maxz)) % maxz
        else: return z % maxz
    return grid[(c(x, maxx), c(y,maxy))]

def walk(grid, maxx, maxy, start, steps):
    reachable_plots = set()
    reachable_plots.add(start)
    for _ in range(steps):
        next_reachable_plots = set()
        while reachable_plots:
            cur_plot = reachable_plots.pop()
            for dir in [UP, DOWN, LEFT, RIGHT]:
                nx,ny = update_loc(cur_plot, dir)
                if nx < 0:
                    val = get_point(grid, nx, ny, maxx, maxy)
                if get_point(grid, nx, ny, maxx, maxy) == '.': next_reachable_plots.add((nx,ny))
        reachable_plots = next_reachable_plots.copy()
    return reachable_plots

def calcb(grid, maxx, maxy, start, steps):
    # Solve for a quadratic: ax^2 + bx + c
    remainder = steps % maxx
    ans = [0,0,0]
    for i in range(3):
        nsteps = remainder + maxx*i
        ans[i] = len(walk(grid, maxx, maxy, start, nsteps))
        print('>', nsteps, ':', ans[i])
    a = (ans[0] - 2*ans[1] + ans[2]) / 2
    b = (-3*ans[0] + 4*ans[1] - ans[2]) / 2
    c = ans[0]
    x = steps // maxx
    return a*x*x + b*x + c 

def grid_print(grid, xr, yr, maxx, maxy, plots):
    out = ''
    for y in range(*yr):
        for x in range(*xr):
            c = get_point(grid, x, y, maxx, maxy)
            if (x,y) in plots:
                c = 'O'
            out += c
        out += '\n'
    print(out)

with open(inputfile()) as f:
    input = getinput(f)

    # Part A
    grid, start = grid_parse(input, True)
    maxx, maxy = len(input[0]), len(input)
    reachable_plots = walk(grid, maxx, maxy, start, steps=64)
    print('Part A: %i' % len(reachable_plots))

    # Part B
    grid, start = grid_parse(input, False)
    total_reachable_plotsb = calcb(grid, maxx, maxy, start, steps=458)
    print('Part B: %i' % total_reachable_plotsb)

#def notes(): For the general problem without math, do something like this...
    #def plot_count(grid_key):
    #    return grid_key.count('O')
    # we only need to calculate how many boundary plots there are, the
    # middle ones 'vibrate' between 2 states
    # So the sum of reachable points = N*full_grids[0] + M*full_grids[1] + boundary_points
    #full_grids = {0: ['', 0], 1: ['', 0]} # full at t % 2 == 0 and t % 2 == 1 -> (key, count)
    #grid_lookup = {} # grid_key(grid) -> (next_grid, last_occurence)
    #blank_grid_key = grid_key(grid, maxx, maxy, set())
    #boundary_grids = defaultdict(lambda: blank_grid_key) # subgridx/y -> grid key
    #boundary_grids[(0,0)] = blank_grid_key
    #for _ in range(steps):
    #    pass
    #extra_plots = 0 # sum of the boundary grids plots
    #return plot_count(full_grids[0][0])*full_grids[0][1] + plot_count(full_grids[1][0])*full_grids[1][1] + extra_plots
    