import math

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
def shoelace(path):
    sum = 0
    for i in range(len(path)):
        x1, y1 = path[i]
        x2, y2 = path[(i+1) % len(path)]
        sum += x1 * y2 - y1 * x2
    area = abs(sum / 2)
    return 1 + area - len(path) / 2

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
