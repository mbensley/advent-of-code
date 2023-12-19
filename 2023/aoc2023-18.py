# Timings: Untimed
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read().splitlines()

def get_route(input):
    sx,sy = 0,0
    route = [(sx,sy)]
    route_len = 0
    for line in input:
        dir, dist, _ = line.split(' ')
        dist = int(dist)
        route_len += dist
        for i in range(dist):
            if dir == 'R':
                sx +=1
            if dir == 'L':
                sx -= 1
            if dir == 'U':
                sy -= 1
            if dir == 'D':
                sy += 1
            route.append((sx,sy))
    return route, route_len

def get_routeb(input):
    def cdir(c):
        return {0:'R', 1:'D', 2:'L', 3:'U'}[c]
    def hdist(hex):
        return int(hex, 16)
    sx,sy = 0,0
    route = [(sx,sy)]
    route_len = 0
    for line in input:
        _, _, hex = line.split(' ')
        dist = hdist(hex[2:7])
        dir = cdir(int(hex[7]))
        dist = int(dist)
        route_len += dist
        for i in range(dist):
            if dir == 'R':
                sx +=1
            if dir == 'L':
                sx -= 1
            if dir == 'U':
                sy -= 1
            if dir == 'D':
                sy += 1
            route.append((sx,sy))
    return route, route_len

# Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
# Sum over all the points that make up the polygon/route
def shoelace(path):
    sum = 0
    for i in range(len(path)):
        x1, y1 = path[i]
        x2, y2 = path[(i+1) % len(path)]
        sum += x1 * y2 - y1 * x2
    area = abs(sum / 2)
    return 1 + area - (len(path)) / 2

with open(inputfile()) as f:
    input = getinput(f)

    # Build the route
    route,route_len = get_route(input)
    routeb, routeb_len = get_routeb(input)

    print('Part A: %i' % (1+shoelace(route)+route_len) )
    print('Part B: %i' % (1+shoelace(routeb)+routeb_len))