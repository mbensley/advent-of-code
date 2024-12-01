import math
from heapq import heappush, heappop

# https://en.wikipedia.org/wiki/Chinese_remainder_theorem

def computeGCD(x, y):
    # use math.gcd(integer iterable)!
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if ((x % i == 0) and (y % i == 0)):
            gcd = i
    return gcd

def lcm(x,y):
    # use math.lcm(integer iterable)
    return (x*y) / computeGCD(x,y)


def get_mdist(sx, sy, bx, by):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(sx-bx) + abs(sy-by)


def get_ldist(sx, sy, bx, by):
    # https://en.wikipedia.org/wiki/Chebyshev_distance
    return max(abs(sx-bx), abs(sy-by))


def tsum(t0, t1, subtract=False):
    # Tuple Sum/Difference
    return [x+y if not subtract else x-y for x, y in zip(t0[:], t1[:])]

def xor(a, b):
    return (a and not b) or (not a and b)

# Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
# Sum over all the points that make up the polygon/route
# Given an ascii-art 'thick' path around a bounding region, this
# returns the A term from Pick's Theorem. https://en.wikipedia.org/wiki/Pick%27s_theorem
def shoelace(path):
    sum = 0
    for i in range(len(path)):
        x1, y1 = path[i]
        x2, y2 = path[(i+1) % len(path)]
        sum += x1 * y2 - y1 * x2
    area = abs(sum) // 2

def get_full_area_with_perimiter(path):
    # Pick's Theoem is A = i + b/2 -1
    # i = A + 1 - b/2
    A = shoelace(path)
    i = A + 1 - len(path) / 2
    return i + len(path) # internal points 

# From the 0th, 1st, and 2nd point
# ans is a triple of values for f(0), f(1), and f(2)
def calc_quadratic_from_3_points(ans, x):
    a = (ans[0] - 2*ans[1] + ans[2]) / 2
    b = (-3*ans[0] + 4*ans[1] - ans[2]) / 2
    c = ans[0]
    return a*x*x + b*x + c 

# Grid Things
def grid_print(grid, maxx, maxy):
    out = ''
    for y in range(maxy):
        for x in range(maxx):
            out += grid[(x,y)]
        out += '\n'
    print(out)

def grid_hash(grid, cols, rows):
    out = ''
    for r in range(rows):
        for c in range(cols):
            out += grid[(r,c)]
        out += '\n'
    return out

def grid_count(grid, maxx, maxy, sym):
    ct = 0
    for y in range(maxy):
        for x in range(maxx):
            if grid[(x,y)] == sym:
                ct += 1
    return ct

def grid_flood(grid, x, y, mx,my, sym='.', osym = 'O'):
    def getcons(xx,yy, seen):
        # foundout = False
        c = []
        dirs = [(xx,yy-1), (xx,yy+1), (xx+1,yy), (xx-1, yy)]
        for d in dirs:
            xx,yy = d
            if xx < -1 or yy < -1 or xx > mx or yy > my:
                continue
            if grid[d] in sym and d not in seen:
                c.append(d)
        return c

    seen = []
    connections = getcons(x,y, seen)
    seen.extend(connections)
    while len(connections) > 0:
        ncx,ncy = connections.pop()
        cs = getcons(ncx,ncy,seen)
        connections.extend(cs)
        seen.extend(cs)
    return seen

def grid_update_loc(loc, dir):
    dmap = {UP: (0,-1), DOWN: (0,1), RIGHT: (1,0), LEFT: (-1,0)}
    x,y = loc
    xx,yy = dmap[dir]
    return (x+xx, y+yy)

UP, RIGHT, LEFT, DOWN = '^', '>', '<', 'v'
# min/max_dist: how far must/can you travel in one direction
def grid_dijkstra(grid, start_point, end_point, min_dist, max_dist):
    def get_new_dir(p, d):
        if d in (UP, DOWN): return (LEFT, RIGHT)
        return (UP, DOWN)

    visited = {} # (point, dir): cost
    point_q = []
    initial_cost = 0
    for dir in (UP, DOWN, LEFT, RIGHT):
        heappush(point_q, (initial_cost, start_point, dir))
    while point_q:
        cost, point, pdir = heappop(point_q)
        if (point, pdir) in visited and visited[(point, pdir)] <= cost:
           continue
        if point == end_point: return cost
        visited[(point, pdir)] = cost
        for newdir in get_new_dir(point, pdir):
            new_point = point
            new_cost = cost
            for icap in range(max_dist):
                new_point = grid_update_loc(new_point, newdir)
                if new_point not in grid: break
                new_cost += grid[new_point]
                if icap+1 >= min_dist:
                    heappush(point_q, (new_cost, new_point, newdir))
    raise # No solution :(
