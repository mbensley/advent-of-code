from collections import defaultdict
import os
from itertools import combinations
from itertools import count


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = []
    return test_input if test else f.read().splitlines()

def calc_antinode_locations(antenna_list, antinode_map, grid, harmonics):
    for freq, pos_list in antenna_list.items():
        for p0, p1 in combinations(pos_list, 2):
            if harmonics:
                antinode_map[freq].update([p0,p1])
            for i in count(start = 1):
                xdist = i*(p0[0] - p1[0])
                ydist = i*(p0[1] - p1[1])
                pa, pb = (0,0), (0,0)
                # Alternatively just calculate the slope of the line
                # and generate the points before and after p0 and p1
                if xdist < 0: # p0 is leftmost
                    leftx = p0[0] - abs(xdist)
                    rightx = p1[0] + abs(xdist)
                else:
                    leftx = p1[0] - abs(xdist)
                    rightx = p0[0] + abs(xdist)
                if ydist < 0: # p0 is topmost
                    topy = p0[1] - abs(ydist)
                    bottomy = p1[1] + abs(ydist)
                else:
                    topy = p1[1] - abs(ydist)
                    bottomy = p0[1] + abs(ydist)
                
                # We now have all 4 new x and y coordinates
                # depending on the position of p0 and p1,
                # there are 4 different orientations for pa and pb.
                if xdist <= 0 and ydist <= 0:
                    pa = (leftx, topy)
                    pb = (rightx, bottomy)
                if xdist <= 0 and ydist > 0:
                    pa = (leftx, bottomy)
                    pb = (rightx, topy)
                if xdist > 0 and ydist <= 0:
                    pa = (rightx, topy)
                    pb = (leftx, bottomy)
                if xdist > 0 and ydist > 0:
                    pa = (rightx, bottomy)
                    pb = (rightx, topy)
                
                in_bounds_nodes = 0
                if grid[pa] != OUT_OF_BOUNDS:
                    antinode_map[freq].add((pa))
                    in_bounds_nodes += 1
                if grid[pb] != OUT_OF_BOUNDS:
                    antinode_map[freq].add((pb))
                    in_bounds_nodes += 1

                # In Part A, there are at most 2 new nodes
                # In Part B, continue running this until both pa and pb
                # are no longer in the mapped area.
                if not harmonics or in_bounds_nodes == 0: break

OUT_OF_BOUNDS = '~'
with open(inputfile()) as f:
    partA = True
    input = getinput(f)

    grid = defaultdict(lambda: OUT_OF_BOUNDS)
    antenna_map = defaultdict(list) # frequency: [pos0, pos1]
    antinode_map = defaultdict(set) # frequency: set(pos0, pos1)
    for y, line in enumerate(input):
        for x, tile in enumerate(line):
            grid[(x,y)] = tile
            if tile != '.':
                antenna_map[tile].append((((x,y))))

    calc_antinode_locations(antenna_map, antinode_map, grid, harmonics=not partA)
    pos_set = set()
    for key, pos_list in antinode_map.items():
        pos_set.update(pos_list)
    
    print('Total harmonics: %i' % len(pos_set))
