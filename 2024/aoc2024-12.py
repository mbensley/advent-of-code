# Timings: Part A: XX:00 / Part B: XX:00
from collections import defaultdict
import os
from typing import TextIO


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = False) -> list[str]:
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read().splitlines()

def parse_grid(input: list[str]) -> dict[complex, str]:
    grid: dict[complex, str] = defaultdict(lambda: '#')
    for x,l in enumerate(input):
        for y,e in enumerate(l):
            grid[x + y*1j] = e
    return grid

def build_regions(grid: dict[complex, str]) -> list[tuple[str,set[complex]]]:
    region_list: list[tuple[str,set[complex]]] = []
    seen_points: set[complex] = set()
    for e in grid:
        if e in seen_points: continue
        region: set[complex] = set()
        # Search
        q: list[complex] = [e]
        region_name = grid[e]
        while q:
            cur: complex = q.pop()
            if cur in region: continue
            region.add(cur)
            # check all 4 directions for neighbors
            for ne in (1,-1,1j,-1j):
                if cur+ne in region: continue
                if cur+ne not in grid: continue
                if grid.get(cur+ne) != grid[cur]: continue
                q.append(cur+ne)
        seen_points.update(region)
        region_list.append((region_name, region))
    return region_list


def calc_area(region: tuple[str, set[complex]]) -> int:
    return len(region[1])

def calc_perimiter(grid: dict[complex, str], region: tuple[str, set[complex]]) -> int:
    perimiter = 0
    for e in region[1]:
        for ne in (1,-1,1j,-1j):
            if grid.get(e+ne) != grid[e]:
                perimiter += 1
    return perimiter

def calc_sides(grid: dict[complex, str], region: tuple[str, set[complex]]) -> int:
    num_sides = 0

    # count number of vertical sides
    for ne in (1j,-1j):
        edge_location: dict[int, list[int]] = defaultdict(lambda: [])
        for e in region[1]:
                if grid.get(e+ne) != grid[e]:
                    edge_location[int(e.imag+ne.imag)].append(int(e.real))
        for _,v in edge_location.items():
            v.sort()
            diff_list = [1 if y-x > 1 and len(v) > 1 else 0 for x,y in zip(v[:-1],v[1:])]
            num_sides += 1+sum(diff_list)

    # count number of horizontal sides
    for ne in (1,-1):   
        edge_location = defaultdict(lambda: [])
        for e in region[1]:
            if grid.get(e+ne) != grid[e]:
                edge_location[int(e.real+ne.real)].append(int(e.imag))
        for _,v in edge_location.items():
            v.sort()
            diff_list = [1 if (y-x > 1 and len(v) > 1) else 0 for x,y in zip(v[:-1],v[1:])]
            num_sides += 1+sum(diff_list)
    return num_sides

with open(inputfile()) as f:
    input = getinput(f)
    grid = parse_grid(input)
    regions = build_regions(grid)
    print(len(regions))
    cost_a, cost_b  = 0, 0
    for region in regions:
        cost_a += calc_area(region) * calc_perimiter(grid, region)
        cost_b += calc_area(region) * calc_sides(grid, region)

    print('Part A: %i' % cost_a)
    print('Part B: %i' % cost_b)
