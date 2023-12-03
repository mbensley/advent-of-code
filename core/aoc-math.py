def computeGCD(x, y):
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if ((x % i == 0) and (y % i == 0)):
            gcd = i
    return gcd


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