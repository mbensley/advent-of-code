# Timings: Untimed
from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['1,0,1~1,2,1:A']
    return test_input if test else f.read().splitlines()      

def add_bricks(input):
    grid = defaultdict(lambda: '.')
    minheightmap = defaultdict(lambda: 1)
    brick_map = {}
    brick_list = []
    for brick_id, line in enumerate(input):
        if not line: break
        label = '#'
        if ':' in line:
            line, label = line.split(':')
        l,r = line.split('~')
        lc = [int(i) for i in l.split(',')]
        rc = [int(i) for i in r.split(',')]
        minz = min(lc[2], rc[2])
        brick_list.append((minz, brick_id, lc, rc, label))
        brick_list.sort(key=lambda x: x[0])
    for _, brick_id, lc, rc, label in brick_list: 
        for i in range(len(lc)):
            if rc[i] - lc[i] < 0: raise '%i neg' % i
        min_height = 1
        # look for what z height this brick can be added to
        for x in range(lc[0], rc[0]+1):
            for y in range(lc[1], rc[1]+1):
                min_height = max(min_height, minheightmap[(x,y)])
        # then add the brick to the grid
        for x in range(lc[0], rc[0]+1):
            for y in range(lc[1], rc[1]+1):
                for z in range(1+rc[2]-lc[2]):
                    grid[(x,y,z+min_height)] = brick_id
                    minheightmap[(x,y)] = 1+z+min_height

        rc[2] = min_height+(rc[2]-lc[2])
        lc[2] = min_height
        brick_map[brick_id] = (lc, rc, label)
        
    return grid, brick_map

# Print the xy map slices
#  x
# ...
# ... y
# ...
def grid_print(grid, brick_map, maxx, maxy, z_height):
    out = '%s\n' % z_height
    for y in range(maxy):
        for x in range(maxx):
            label = '.'
            if grid[(x,y,z_height)] in brick_map:
                label = get_label(brick_map, grid[(x,y,z_height)])
            if z_height == 0:
                out += '@'
            out += label
        out += '\n'
    print(out)

# dir = 1 for above and -1 for below
def bricks_touching(brick_id, brick_map, grid, dir):
    lc,rc,label = brick_map[brick_id]
    if dir == 1:
        z = rc[2]
    else:
        z = lc[2]
    touching = set()
    for x in range(lc[0],rc[0]+1):
        for y in range(lc[1],rc[1]+1):
            if grid[(x,y,z+dir)] != '.':
                touching.add(grid[(x,y,z+dir)])
    return touching

def get_label(brick_map, brick_id):
    label = str(brick_id)
    if brick_map[brick_id][2] != '#':
        label = brick_map[brick_id][2]
    return label

def can_remove_safely(grid, brick_map, brick_id):
    can_remove = True
    for above_id in bricks_touching(brick_id, brick_map, grid, dir=1):
        can_remove = can_remove and len(bricks_touching(above_id, brick_map, grid, dir=-1)) > 1
        if not can_remove:
            break
    return can_remove

# check all lower bricks supporting this one
# do any of them reach down below the parent brick we're removing?
def has_other_parent_lower(grid, brick_map, brick_id, parent_brick_id, target_z):
    parents = bricks_touching(brick_id, brick_map, grid, dir=-1)
    while parents:
        cur_parent = parents.pop()
        if parent_brick_id == cur_parent:
            continue
        l, r, _ = brick_map[cur_parent]
        minz = min(l[2], r[2])
        if minz <= target_z:
            return True
        parents.update(bricks_touching(cur_parent, brick_map, grid, dir=-1))
    return False

# get everything stacked on top of brick_id
def get_brick_tower(grid, brick_map, brick_id):
    brick_tower = set()
    checklist = bricks_touching(brick_id, brick_map, grid, dir=1)
    while checklist:
        cur_brick = checklist.pop()
        brick_tower.add(cur_brick)
        checklist.update(bricks_touching(cur_brick, brick_map, grid, dir=1))
    return brick_tower

def calc_chain_reaction(grid, brick_map, brick_id):
    # Can Brick A be removed? If yes then nothing falls.
    if can_remove_safely(grid, brick_map, brick_id):
        return 0
    # Otherwise, how many bricks are stacked on A
    # and which of those have a separate 'parent' that doesn't
    # also have A as a parent? and that parent has to have z <= A.z
    brick_tower = get_brick_tower(grid, brick_map, brick_id)
    total = 0 
    parent_brick = brick_map[brick_id] 
    targetz = min(parent_brick[0][2], parent_brick[1][2])
    for brick in brick_tower:
        if not has_other_parent_lower(grid, brick_map, brick, brick_id, targetz):
            total += 1
    return total

with open(inputfile()) as f:
    input = getinput(f)
    grid, brick_map = add_bricks(input)

    print('Part A: %i' % sum([1 for brick_id in brick_map.keys() if can_remove_safely(grid, brick_map, brick_id)]))
    print('Part B: %i' % sum([calc_chain_reaction(grid, brick_map, brick_id) for brick_id in brick_map.keys()]))
