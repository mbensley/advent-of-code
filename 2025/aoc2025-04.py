import os


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')


def getinput(f, test):
    test_input = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    return test_input if test else f.read().splitlines()


def count_lonely_at_signs(grid):
    """
    Generated with Gemini Code Assist 2.5:
    Given a 2D grid of '@' and '.' characters, counts the number of '@'
    characters that have less than 4 other adjacent '@' characters in all 8
    directions and returns that value as an integer.

    For example:
    ..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@.

    should return 13
    """
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    lonely_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                adjacent_at_count = 0
                # Check all 8 directions
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue

                        nr, nc = r + dr, c + dc

                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            adjacent_at_count += 1
                
                if adjacent_at_count < 4:
                    lonely_count += 1
    
    return lonely_count

def lonely_at_sign_solver(grid):
    """
    Generated with Gemini Code Assist 2.5:
    Given a 2D grid of '@' and '.' characters, counts the number of '@' characters
    that have less than 4 other adjacent '@' characters in all 8 directions,
    called a lonley_at_sign.

    For every lonely_at_sign, replace it in the grid with a '.' symbol and
    rerun this process until no more '@' symbols can be removed.

    Then return the total number '@' removed in total as an int.
    """
    if not grid:
        return 0

    # Make a mutable copy of the grid
    mutable_grid = [list(row_str) for row_str in grid]
    rows = len(mutable_grid)
    if rows == 0:
        return 0
    cols = len(mutable_grid[0])
    if cols == 0:
        return 0

    total_removed = 0

    while True:
        to_remove = []
        # Find all lonely '@'
        for r in range(rows):
            for c in range(cols):
                if mutable_grid[r][c] == '@':
                    at_neighbors = 0
                    # Check 8 directions
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Don't count self

                            nr, nc = r + dr, c + dc

                            # Check bounds
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if mutable_grid[nr][nc] == '@':
                                    at_neighbors += 1

                    if at_neighbors < 4:
                        to_remove.append((r, c))

        if not to_remove:
            # No more '@' to remove, we are done.
            break

        # Remove the lonely '@'s
        for r, c in to_remove:
            mutable_grid[r][c] = '.'
        
        total_removed += len(to_remove)

    return total_removed

# To run the test, you can uncomment the following lines:
if __name__ == "__main__":
    test = True
    with open(inputfile()) as f:
        grid_data = getinput(f, test)

    result = count_lonely_at_signs(grid_data)
    print(f"The number of '@' characters with fewer than 4 adjacent '@'s is: {result}")

    if test:
        # Expected output is 13
        assert result == 13, f"Test failed: Expected 13, but got {result}"
        print("Test passed!")
    
    total_removed = lonely_at_sign_solver(grid_data)
    print(f"The total number of '@' characters removed is: {total_removed}")
    if test:
        assert total_removed == 43, f"Test for lonely_at_sign_solver failed: Expected 43, but got {total_removed}"
        print("Test for lonely_at_sign_solver passed!")
