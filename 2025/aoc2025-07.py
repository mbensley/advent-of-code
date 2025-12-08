import os

def solve_a():
    """
    Solves the Advent of Code 2025 Day 7 puzzle.
    """
    input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    with open(input_path, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    start_pos = None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    if not start_pos:
        print("No start position 'S' found in the grid.")
        return

    s_r, s_c = start_pos
    grid[s_r][s_c] = '|'
    flowing_cols = {s_c}

    for r in range(s_r + 1, len(grid)):
        newly_flowing_cols = set()
        for c in sorted(list(flowing_cols)): # sorted to ensure deterministic behavior
            if grid[r][c] == '.':
                grid[r][c] = '|'
                newly_flowing_cols.add(c)
            elif grid[r][c] == '^':
                # Flow hits a '^', splits to the sides on the same row
                if c - 1 >= 0 and grid[r][c-1] == '.':
                    grid[r][c-1] = '|'
                    newly_flowing_cols.add(c-1)
                if c + 1 < len(grid[r]) and grid[r][c+1] == '.':
                    grid[r][c+1] = '|'
                    newly_flowing_cols.add(c+1)
        flowing_cols = newly_flowing_cols

    part_a_count = 0
    for r in range(1, len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '^' and grid[r-1][c] == '|':
                part_a_count += 1
    
    print(f"Part A: {part_a_count}")


def solve_b():
    """
    Solves Part B of the Advent of Code 2025 Day 7 puzzle.
    """
    input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    with open(input_path, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    start_pos = None
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break

    if not start_pos:
        print("No start position 'S' found in the grid.")
        return

    memo = {}

    def count_paths(r, c):
        if (r, c) in memo:
            return memo[(r, c)]

        if not (0 <= c < len(grid[0])):
            return 0  # Out of bounds

        # A path reaching the bottom row is a complete path, so we count it as 1.
        # If we returned 0 as requested, the total count would always be 0.
        if r == len(grid) - 1:
            return 1

        next_r = r + 1
        
        # Ensure we don't go past the bottom of the grid
        if next_r >= len(grid):
            return 1

        below_char = grid[next_r][c]

        if below_char == '.':
            result = count_paths(next_r, c)
        elif below_char == '^':
            result = count_paths(next_r, c - 1) + count_paths(next_r, c + 1)
        else:
            # Path is blocked by something other than '.' or '^'
            result = 0
        
        memo[(r, c)] = result
        return result

    s_r, s_c = start_pos
    total_paths = count_paths(s_r, s_c)
    print(f"Part B: {total_paths}")


solve_a()
solve_b()
