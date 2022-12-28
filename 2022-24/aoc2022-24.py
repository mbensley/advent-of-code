import os
from collections import deque
import sys
from copy import deepcopy


def get_val(point: tuple, grid_rows: list, grid_cols: list) -> tuple:
    # Order: <, >, ^, v
    x, y = point
    return (grid_rows[y][0][x], grid_rows[y][1][x], grid_cols[x][0][y], grid_cols[x][1][y])


def forward(grid_rows: list, grid_cols: list) -> None:
    for ld, rd in grid_rows:
        ld.rotate(1)
        rd.rotate(-1)
    for ud, dd in grid_cols:
        ud.rotate(-1)
        dd.rotate(1)


def get_possible_moves(point: tuple, grid_rows: list, grid_cols: list):
    moves = []
    # check U, D, L, R from point
    if point[1] < len(grid_rows)-1 and len(set(get_val((point[0], point[1]+1), grid_rows, grid_cols))) == 1:
        moves.append('D')
    if point[0] < len(grid_cols)-1 and len(set(get_val((point[0]+1, point[1]), grid_rows, grid_cols))) == 1:
        moves.append('R')
    if point[1] > 0 and len(set(get_val((point[0], point[1]-1), grid_rows, grid_cols))) == 1:
        moves.append('U')
    if point[0] > 0 and point[1] < len(grid_rows) and len(set(get_val((point[0]-1, point[1]), grid_rows, grid_cols))) == 1:
        moves.append('L')
    if point[1] < len(grid_rows) and len(set(get_val((point[0], point[1]), grid_rows, grid_cols))) == 1:
        moves.append('W')

    # print('At %s moves: %s' % (point, moves))
    return moves


def move_pawn(pawn: tuple, move: str) -> tuple:
    if move == 'U':
        pawn = (pawn[0], pawn[1]-1)
    if move == 'D':
        pawn = (pawn[0], pawn[1]+1)
    if move == 'L':
        pawn = (pawn[0]-1, pawn[1])
    if move == 'R':
        pawn = (pawn[0]+1, pawn[1])
    if move == 'W':
        pawn = (pawn[0], pawn[1])
    return pawn


def pretty_print(start_point, end_point, pawn, grid_rows, grid_cols):
    output = ''
    x_len = len(grid_cols)
    for x in range(x_len+1):
        if (x-1, -1) == pawn:
            output += 'E'
        else:
            output += '#' if start_point[0] != x-1 else '.'
    output += '#\n'

    for y in range(len(grid_rows)):
        output += '#'
        for x in range(x_len):
            point_set = set(get_val((x, y), grid_rows, grid_cols))
            if len(point_set) == 1:
                if (x, y) == pawn:
                    output += 'E'
                else:
                    output += '.'
            elif len(point_set) == 2:
                if '<' in point_set:
                    output += '<'
                elif '>' in point_set:
                    output += '>'
                elif '^' in point_set:
                    output += '^'
                else:
                    output += 'v'
            elif len(point_set) == 3:
                output += '2'
            elif len(point_set) == 4 and '.' in point_set:
                output += '3'
            else:
                output += '4'
        output += '#\n'
    for x in range(x_len+1):
        if (x, len(grid_rows)+1) == pawn:
            output += 'E'
        else:
            output += '#' if end_point[0] != x else '.'
    output += '#\n'
    print(output)


def build_grid(lines: list) -> tuple:
    # elements are <, >
    grid_rows = []
    # elements are ^, v
    grid_cols = []
    for x, c in enumerate(lines[0]):
        if c == '.':
            start_point = (x-1, -1)
    for x, c in enumerate(lines[-1]):
        if c == '.':
            end_point = (x-1, len(lines)-2)
    # >,< deque
    for row in lines[1:-1]:
        grid_rows.append((deque(row.replace('<', '.').replace('^', '.').replace('v', '.').replace('#', '')),
                         deque(row.replace('>', '.').replace('^', '.').replace('v', '.').replace('#', ''))))
    # ^,v deque
    for x in range(1, len(lines[0])-1, 1):
        d_up = deque()
        d_down = deque()
        for line in lines[1:-1]:
            if line[x] == '#':
                continue
            elif line[x] == '^':
                d_up.append('^')
                d_down.append('.')
            elif line[x] == 'v':
                d_up.append('.')
                d_down.append('v')
            else:
                d_up.append('.')
                d_down.append('.')
        grid_cols.append((d_up, d_down))
    return start_point, end_point, grid_rows, grid_cols


def find_path_rec(pawn: tuple, start_point: tuple, end_point: tuple, grid_rows: list, grid_cols: list, move_num: int):
    if move_num % 500 == 0:
        print('Depth: %i' % move_num)
        pretty_print(start_point, end_point, pawn, grid_rows, grid_cols)
    if pawn == end_point:
        print('Found exit: %i ' % move_num)
        return move_num
    total_moves = move_num
    moves = get_possible_moves(pawn, grid_rows, grid_cols)
    if len(moves) == 0:
        print('found unreachable path %i' % move_num)
        return 999999999
    for move in moves:
        pawn = move_pawn(pawn, move)
        total_moves = min(total_moves, find_path(
            pawn, start_point, end_point, deepcopy(grid_rows), deepcopy(grid_cols), move_num+1))
    return total_moves


def find_path(start_point: tuple, end_point: tuple, grid_rows: list, grid_cols: list, max_time: int) -> int:
    print('Start %s' % str(start_point))
    print('Looking for end point: %s' % str(end_point))
    points = set([start_point])
    for t in range(0, max_time, 1):
        new_points = set()
        for point in points:
            for move in get_possible_moves(point, grid_rows, grid_cols):
                new_point = move_pawn(point, move)
                if new_point == (end_point[0], end_point[1]-1) or new_point == (end_point[0], end_point[1]+1):
                    forward(grid_rows, grid_cols)
                    return t+1
                new_points.add(new_point)
        points = new_points
        forward(grid_rows, grid_cols)
        if len(points) == 0:
            points.add(start_point)
    raise Exception('No path found within %i rounds' % max_time)


test = False
filename = '/2022-24/input-t.txt' if test else '/2022-24/input.txt'
with open(os.getcwd() + filename) as f:
    lines = f.read().splitlines()
    start_point, end_point, grid_rows, grid_cols = build_grid(lines)
    pretty_print(start_point, end_point, start_point, grid_rows, grid_cols)
    max_time = 1000
    s_to_e = find_path(start_point, end_point, grid_rows, grid_cols, max_time)
    e_to_s = find_path(end_point, start_point, grid_rows, grid_cols, max_time)
    s_to_e2 = find_path(start_point, end_point, grid_rows, grid_cols, max_time)
    print('Part A: %i' % s_to_e)
    print('Part B: %i %i %i = %i' %
          (s_to_e, e_to_s, s_to_e2, (s_to_e + e_to_s + s_to_e2)))

    # for a 5x5 full pattern repeats every 5 ticks
