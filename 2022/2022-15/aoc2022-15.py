import os
from collections import defaultdict


def get_mdist(sx, sy, bx, by):
    # https://en.wikipedia.org/wiki/Taxicab_geometry
    return abs(sx-bx) + abs(sy-by)


def get_ldist(sx, sy, bx, by):
    # https://en.wikipedia.org/wiki/Chebyshev_distance
    return max(abs(sx-bx), abs(sy-by))


def build_grid(locations):
    grid = defaultdict(lambda: '.')
    for sensor, beacon in locations:
        grid[sensor] = 'S'
        grid[beacon] = 'B'
    return grid


def parse_input(lines):
    # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    locations = []
    for line in lines:
        sensor, beacon = line.split(': ')
        sensorx, sensory = sensor.split(', ')
        sx = int(str(sensorx.split('=')[1][:]))
        sy = int(sensory.split('=')[1][:])
        beacx, beacy = beacon.split(', ')
        bx = int(beacx.split('=')[1][:])
        by = int(beacy.split('=')[1][:])
        locations.append(((sx, sy), (bx, by)))
    return locations


def cover(point, grid: dict, locations: list):
    if grid[point] in ['B', 'S', '#']:
        return
    for sensor, beacon in locations:
        r = get_mdist(*sensor, *beacon)
        pr = get_mdist(*sensor, *point)
        if pr <= r:
            pixel = grid[point]
            if pixel == '.':
                grid[point] = '#'


def get_window(yloc, locations: list):
    minx = float('inf')
    maxx = -float('inf')
    for sensor, beacon in locations:
        r = get_mdist(*sensor, *beacon)
        minx_seen = sensor[0] - r
        maxx_seen = sensor[0] + r
        minx = min(minx, minx_seen)
        maxx = max(maxx, maxx_seen)
    return minx, maxx


def get_xslice(y: int, sx, sy, dist):
    ydist = get_mdist(sx, sy, sx, y)
    # check that interects y
    if ydist <= dist:
        xunits = abs(dist - ydist)
        return sorted((sx-xunits, sx+xunits))
    return None, None


def is_overlap(sa, ea, sb, eb):
    # either sa is in range of B or sb is in range of A
    return (eb >= sa >= sb) or (ea >= sb >= sa)


def is_range_contained(sa, ea, sb, eb):
    #   sa      ea
    #      sb eb
    return (sa <= sb and ea >= eb) or (sb <= sa and eb >= ea)


def merge_ranges(r0, r1):
    r0min, r0max = r0
    r1min, r1max = r1
    return min(r0min, r1min), max(r0max, r1max)


def add_range(new_range, ranges: list) -> list:
    if not ranges:
        return [new_range]

    new_ranges = []
    nl, nr = new_range
    for i, (rl, rr) in enumerate(ranges):
        if nr < rl:
            new_ranges.append((nl, nr))
            new_ranges.extend(ranges[i:])
            return new_ranges
        if is_overlap(nl, nr, rl, rr) or is_range_contained(nl, nr, rl, rr):
            nl, nr = merge_ranges((nl, nr), (rl, rr))
        else:
            new_ranges.append((rl, rr))
    new_ranges.append((nl, nr))
    return new_ranges


def count_coverage(range_list, hardware_set):
    total_range = []
    count = 0
    for r in range_list:
        total_range = add_range(r, total_range)
    # sum of all the ranges
    for rl, rr in total_range:
        count += abs(rr - rl+1)
    # remove the beacon and sensor spots
    hardware_count = 0
    for bx, by in hardware_set:
        for rl, rr in total_range:
            if is_overlap(bx, bx, rl, rr):
                hardware_count += 1
    return count, hardware_count


with open(os.getcwd() + '/2022-15/input.txt') as f:
    locations = parse_input(f.read().splitlines())
    grid = build_grid(locations)
    parta_slow, parta_fast, part_b = False, False, True
    if parta_slow:
        yloc = 2000000
        minx, maxx = float('inf'), -float('inf')
        filtered_locations = []
        for sensor, beacon in locations:
            sminx, smaxx = get_xslice(
                yloc, *sensor, get_mdist(*sensor, *beacon))
            if sminx:
                minx = min(minx, sminx)
                maxx = max(maxx, smaxx)
                print('[%i, %i]' % (sminx, smaxx))
                filtered_locations.append((sensor, beacon))

        print('range of x: [%i,%i]' % (minx, maxx))
        for x in range(minx, maxx+1):
            cover((x, yloc), grid, filtered_locations)
        count = 0
        for key, pixel in filter(lambda items: items[0][1] == yloc, grid.items()):
            if pixel == '#':
                count += 1

        print('Part A: %i' % count)
    if parta_fast:
        yloc = 2000000
        range_list = []
        hardware_set = set()
        for sensor, beacon in locations:
            hardware_set.add(beacon)
            hardware_set.add(sensor)
            sminx, smaxx = get_xslice(
                yloc, *sensor, get_mdist(*sensor, *beacon))
            if sminx:
                print('[%i, %i]' % (sminx, smaxx))
                range_list.append((sminx, smaxx))
        f_hardware = [b for b in filter(
            lambda x: x[1] == yloc, hardware_set)]
        count, hardware_count = count_coverage(range_list, f_hardware)
        print('Part A: %i' % (count-hardware_count))
    if part_b:
        # part_b_fast: check only the points along the perimiter of each exclusion zone
        # instead of checking every point along each slice
        search_x_min = 0
        search_x_max = 4000000
        search_y_min = 3042458 - 1
        search_y_max = search_y_min + 2
        for yloc in range(search_y_min, search_y_max):
            if yloc % 100000 == 0:
                print('y %i' % yloc)
            range_list = []
            hardware_set = set()
            for sensor, beacon in locations:
                hardware_set.add(beacon)
                hardware_set.add(sensor)
                sminx, smaxx = get_xslice(
                    yloc, *sensor, get_mdist(*sensor, *beacon))
                if sminx != None:
                    minx = max(sminx, 0)
                    maxx = min(smaxx, search_x_max)
                    range_list.append((minx, maxx))
            f_hardware = [b for b in filter(
                lambda x: x[1] == yloc, hardware_set)]
            count, hardware_count = count_coverage(range_list, f_hardware)
            if count != search_x_max+1:
                print('found incorrect count %i, yloc %i' % (count, yloc))
                total_range = []
                for r in range_list:
                    total_range = add_range(r, total_range)
                print(total_range)
                print('Part B: %i' % (((total_range[0][1]+1)*4000000)+yloc))
