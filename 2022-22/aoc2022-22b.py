import os
import re


def get_next_point(pawn: list, board: dict, len_side: int):
    if board[pawn[0]] not in ['.', '#']:
        raise
    # point: complex, dir: int
    direction = pawn[1]
    start = pawn[0]
    delta = (complex(1, 0), complex(0, 1),
             complex(-1, 0), complex(0, -1))[direction]
    if start+delta not in board or board[start+delta] == ' ':
        adj_point, adj_dir = get_adjacent_point(pawn, delta, board, len_side)
        print('pawn: %s delta: %s' % (pawn, delta))
        print('adj_point: %s' % str(adj_point))
        if peek(adj_point, board) == '.':
            return adj_point, adj_dir
        return start, direction
    elif peek(start+delta, board) == '.':
        return start+delta, direction
    elif peek(start+delta, board) == '#':
        return start, direction
    raise


def get_side_test(point: complex, len_side: int) -> int:
    if point.real < len_side:
        side = 2
    elif len_side <= point.real < len_side*2:
        side = 3
    elif 3*len_side <= point.real:
        side = 6
    elif int(point.imag) < len_side:
        side = 1
    elif len_side <= int(point.imag) < 2*len_side:
        side = 4
    else:
        side = 5
    return side


def get_side(point: complex, len_side: int) -> int:
    if point.real >= 2*len_side:
        return 2
    if int(point.imag) >= 3*len_side:
        return 6
    if 2*len_side > int(point.imag) >= len_side:
        return 3
    if point.real < len_side:
        return 4
    if 2*len_side <= int(point.imag) < 3*len_side:
        return 5
    return 1


def get_adjacent_point(pawn, delta: complex, board: dict, len_side: int):
    # find your side
    side = get_side(pawn[0], len_side)
    direction = pawn[1]
    start = pawn[0]
    print('start: %s dir: %s side: %s' % (str(start), direction, side))
    if side == 1:
        if direction == 2:  # Left -> 4L
            nx = 0
            ny = 3*len_side - int(start.imag) - 1
            d = 0
            if get_side(complex(nx, ny), len_side) != 4:
                raise
        if direction == 3:  # Up -> 6L
            nx = 0
            ny = 3*len_side + (int(start.real) % len_side)
            d = 0
            if get_side(complex(nx, ny), len_side) != 6:
                raise
    if side == 2:
        if direction == 0:  # Right -> 5R
            nx = 2*len_side - 1
            ny = 3*len_side - int(start.imag) - 1
            d = 2
            if get_side(complex(nx, ny), len_side) != 5:
                raise
        if direction == 1:  # Down -> 3R
            nx = 2*len_side - 1
            ny = len_side + (start.real % len_side)
            d = 2
            if get_side(complex(nx, ny), len_side) != 3:
                raise
        if direction == 3:  # Up -> 6D
            nx = start.real % len_side
            ny = 4*len_side - 1
            d = 3
            if get_side(complex(nx, ny), len_side) != 6:
                raise
    if side == 3:
        if direction == 0:  # Right -> 2D
            nx = 2*len_side + (int(start.imag) % len_side)
            ny = len_side - 1
            d = 3
            if get_side(complex(nx, ny), len_side) != 2:
                raise
        if direction == 2:  # Left -> 4U
            nx = int(start.imag) % len_side
            ny = 2*len_side
            d = 1
            if get_side(complex(nx, ny), len_side) != 4:
                raise
    if side == 4:
        if direction == 2:  # Left -> 1L
            nx = len_side
            ny = len_side - (int(start.imag) % len_side) - 1
            d = 0
            if get_side(complex(nx, ny), len_side) != 1:
                raise
        if direction == 3:  # Up -> 3L
            nx = len_side
            ny = len_side + int(start.real)
            d = 0
            if get_side(complex(nx, ny), len_side) != 3:
                raise
    if side == 5:
        if direction == 0:  # Right -> 2R
            nx = 3*len_side - 1
            ny = len_side - (int(start.imag) % len_side) - 1
            d = 2
            if get_side(complex(nx, ny), len_side) != 2:
                raise
        if direction == 1:  # Down -> 6R
            nx = len_side - 1
            ny = 3*len_side + (start.real % len_side)
            d = 2
            if get_side(complex(nx, ny), len_side) != 6:
                raise
    if side == 6:
        if direction == 0:  # Right -> 5D
            nx = len_side + (int(start.imag) % len_side)
            ny = 3*len_side - 1
            d = 3
            if get_side(complex(nx, ny), len_side) != 5:
                raise
        if direction == 1:  # Down -> 2U
            nx = 2*len_side + (start.real)
            ny = 0
            d = 1
            if get_side(complex(nx, ny), len_side) != 2:
                raise
        if direction == 2:  # Left -> 1U
            nx = len_side + (int(start.imag) % len_side)
            ny = 0
            d = 1
            if get_side(complex(nx, ny), len_side) != 1:
                raise
    return complex(nx, ny), d


def get_adjacent_point_test(pawn, delta: complex, board: dict, len_side: int):
    # find your side
    side = get_side(pawn[0], len_side)
    direction = pawn[1]
    # each side has a different mapping
    if side == 1:  # Right, Left, Up
        print('in side %i: %s' % (side, pawn))
        if direction == 0:  # right, move to side 6
            new_xval = 4*len_side - 1
            new_yval = (4*len_side) - (int(pawn[0].imag) % len_side) - 1
            return complex(), 2
        if direction == 2:  # left move to side 3
            new_xval = len_side + (int(pawn[0].imag) % len_side)
            new_yval = len_side - 1
            return complex(new_xval, new_yval), 1
        if direction == 3:  # up move to side 2
            new_xval = len_side - (int(pawn[0].real) % len_side) - 1
            new_yval = len_side - 1
            return complex(new_xval, new_yval), 1
    if side == 2:  # Down, Left, Up
        print('in side %i: %s' % (side, pawn))
        if direction == 1:  # Down, move to side 5
            new_xval = (3*len_side) - (int(pawn[0].real) % len_side) - 1
            new_yval = 3*len_side - 1
            return complex(new_xval, new_yval), 3
        if direction == 2:  # Left, move to side 6
            new_xval = (4*len_side) - (int(pawn[0].imag) % len_side) - 1
            new_yval = 3*len_side - 1
            return complex(new_xval, new_yval), 3
        if direction == 3:  # Up, move to side 1
            new_xval = (2*len_side) + (int(pawn[0].real) % len_side)
            new_yval = 0
            return complex(new_xval, new_yval), 1
    if side == 3:  # Down, Up
        print('in side %i: %s' % (side, pawn))
        if direction == 1:  # Down move to side 5
            new_xval = 2*len_side
            new_yval = (3*len_side) - (int(pawn[0].real) % len_side) - 1
            return complex(new_xval, new_yval), 0
        if direction == 3:  # Up, move to side 1
            new_xval = 2*len_side
            new_yval = (int(pawn[0].real) % len_side)
            return complex(new_xval, new_yval), 0
    if side == 4:  # only wrap is dir == 0, move to 6
        print('in side %i: %s' % (side, pawn))
        new_xval = (4*len_side) - (int(pawn[0].imag) % len_side) - 1
        new_yval = 2*len_side
        return complex(new_xval, new_yval), 1
    if side == 5:  # Down, Left
        print('in side %i: %s' % (side, pawn))
        if direction == 1:  # Down, move to side 2
            new_xval = len_side - (int(pawn[0].real) % len_side) - 1
            new_yval = 2*len_side - 1
            return complex(new_xval, new_yval), 3
        if direction == 2:  # Left, move to side 3
            new_xval = (2*len_side) - (int(pawn[0].imag) % len_side) - 1
            new_yval = 2*len_side - 1
            return complex(new_xval, new_yval), 3
    if side == 6:  # Up, Right, Down
        print('in side %i: %s' % (side, pawn))
        if direction == 0:  # Right, move to side 1
            new_xval = 3*len_side - 1
            new_yval = len_side - (int(pawn[0].imag) % len_side) - 1
            return complex(new_xval, new_yval), 2
        if direction == 1:  # Down, move to side 2
            new_xval = 0
            new_yval = (2*len_side) + (int(pawn[0].real) % len_side) - 1
            return complex(new_xval, new_yval), 0
        if direction == 3:  # Up, move to side 4
            new_xval = 3*len_side - 1
            new_yval = (2*len_side) + (int(pawn[0].real) % len_side) - 1
            return complex(new_xval, new_yval), 2
    print('point: %s, side: %i, dir: %s' % (pawn[0], side, str(direction)))
    raise


def peek(point: complex, board: dict) -> str:
    return board[point]


def get_first_point_col(point: complex, board: dict) -> complex:
    for y in range(int(point.imag)):
        np = complex(point.real, y)
        if board[np] in ['.', '#']:
            return np


def get_first_point_row(point: complex, board: dict) -> complex:
    for x in range(int(point.real)):
        np = complex(x, point.imag)
        if board[np] in ['.', '#']:
            return np


def get_last_point_col(point: complex, board: dict) -> complex:
    max_y = max(int(p.imag) for p in board.keys())
    for y in range(max_y, -1, -1):
        np = complex(point.real, y)
        if board[np] in ['.', '#']:
            return np


def get_last_point_row(point: complex, board: dict) -> complex:
    max_x = max(int(p.real) for p in board.keys())
    for x in range(max_x, -1, -1):
        np = complex(x, point.imag)
        if board[np] in ['.', '#']:
            return np


test_input = False
filename = '/2022-22/input-t.txt' if test_input else '/2022-22/input.txt'
with open(os.getcwd() + filename) as f:
    board = {}
    len_side = 4 if test_input else 50
    brows, inst = f.read().split('\n\n')
    for y, row in enumerate(brows.splitlines()):
        for x, c in enumerate(row):
            board[complex(x, y)] = c
    max_x = max(int(p.real) for p in board.keys())
    max_y = max(int(p.imag) for p in board.keys())
    # for y in range(max_y+1):
    #    for x in range(max_x+1):
    #        if complex(x, y) not in board:
    #            board[complex(x, y)] = ' '
    instructions = re.findall(r'(\d+|[RL]+)', inst)
    start_pos = complex(0, 0)
    for x in range(max(int(c.real) for c in board.keys())):
        if board[complex(x, 0)] == '.':
            start_pos = complex(x, 0)
            break
    # heading = R:0,D:1,L:2,U:3
    pawn = [start_pos, 0]
    for i in instructions:
        if i[0] in '1234567890':
            moves = int(i)
            for _ in range(moves):
                pawn[0], pawn[1] = get_next_point(pawn, board, len_side)
        else:  # change heading
            if i == 'R':
                pawn[1] = (pawn[1]+1) % 4
            if i == 'L':
                pawn[1] = (pawn[1]-1) if pawn[1] > 0 else 3

    print(pawn)
    print((int(pawn[0].imag)+1)*1000 + (pawn[0].real+1)*4 + pawn[1])
