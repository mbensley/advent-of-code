from collections import defaultdict
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=True):
    test_input = [
        'MMMSXXMASM',
        'MSAMXMSMSA',
        'AMXSXMAAMM',
        'MSAMASMSMX',
        'XMASAMXAMM',
        'XXAMMXXAMA',
        'SMSMSASXSS',
        'SAXAMASAAA',
        'MAMMMXMMMM',
        'MXMXAXMASX']
    return test_input if test else f.read().splitlines()

def find_word_count(grid, word, maxx, maxy):
    # left, right, up, down, diag_l_up, diag_r_up, diag_l_d, diag_r_d
    dir_list = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (-1,1), (1,1)]

    def build_word(start, dir):
        new_word = []
        loc = start
        for i in range(len(word)):
            new_word.append(grid[(start[0] + i*dir[0], start[1] + i*dir[1])])
        return ''.join(new_word)

    # Check for the word at all locations
    total = 0
    for y in range(maxy):
        for x in range(maxx):
            if grid[(x,y)] == word[0]:
                for dir in dir_list:
                    test_word = build_word((x,y), dir)
                    if test_word == word:
                        total += 1
    return total

def find_mas_count(grid, word, maxx, maxy):
    def build_word(axy, m, s):
        ax,ay = axy
        mx,my = ax+m[0], ay+m[1]
        sx,sy = ax+s[0], ay+s[1]
        return grid[(mx,my)] + grid[(ax,ay)] + grid[(sx,sy)]
    
    # 4 configurations for where M can be: TT, BB, LL, RR
    # (M,S,M1,S1)
    dir_list = [((-1,-1),(1,1),(1,-1),(-1,1)), # TT
                ((-1,1),(1,-1),(1,1),(-1,-1)), # BB
                ((-1,-1),(1,1),(-1,1),(1,-1)), # LL
                ((1,-1),(-1,1),(1,1),(-1,-1))] # RR
    def check(start):
        for m0,s0,m1,s1 in dir_list:
            if build_word(start, m0, s0) == word and build_word(start, m1, s1) == word:
                return True

    total = 0
    for y in range(maxy):
        for x in range(maxx):
            if grid[(x,y)] == word[1]: # Build words based on the middle A
                if check((x,y)):
                    total += 1
    return total

with open(inputfile()) as f:
    input = getinput(f)
    grid = defaultdict(lambda: '.')
    for y, line in enumerate(input):
        for x, val in enumerate(line):
            grid[(x,y)] = val

    print('Part A: %i' % find_word_count(grid, 'XMAS', len(input), len(input[0])))
    print('Part B: %i' % find_mas_count(grid, 'MAS', len(input), len(input[0])))
