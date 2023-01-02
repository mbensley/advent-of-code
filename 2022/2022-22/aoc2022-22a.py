import os
import re


def get_next_point(pawn: list, board: dict) -> complex:
    if board[pawn[0]] not in ['.', '#']:
        raise
    # point: complex, dir: int
    dir = pawn[1]
    start = pawn[0]
    delta = (complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1))[dir]
    if start+delta not in board or board[start+delta] == ' ':
        if dir == 0:
            first_point = get_first_point_row(start+delta, board)
            if peek(first_point, board) == '.':
                return first_point
            return pawn[0]
        if dir == 1:
            first_point = get_first_point_col(start+delta, board)
            if peek(first_point, board) == '.':
                return first_point
            return pawn[0]
        if dir == 2:
            first_point = get_last_point_row(start+delta, board)
            if peek(first_point, board) == '.':
                return first_point
            return pawn[0]
        if dir == 3:
            first_point = get_last_point_col(start+delta, board)
            if peek(first_point,  board) == '.':
                return first_point
            return pawn[0]
    elif peek(start+delta, board) == '.':
        return start+delta
    elif peek(start+delta, board) == '#':
        return start
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


test_input = True
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
    for y in range(max_y+1):
        for x in range(max_x+1):
            if complex(x, y) not in board:
                board[complex(x, y)] = ' '
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
                pawn[0] = get_next_point(pawn, board)
        else:  # change heading
            if i == 'R':
                pawn[1] = (pawn[1]+1) % 4
            if i == 'L':
                pawn[1] = (pawn[1]-1) if pawn[1] > 0 else 3

    print(pawn)
    print((int(pawn[0].imag)+1)*1000 + (pawn[0].real+1)*4 + pawn[1])
