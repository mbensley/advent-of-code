import os
import itertools

def solve_a():
    """
    Solves Part A of the Advent of Code 2025 Day 9 puzzle.
    """
    
    # --- Input Handling ---
    use_file_input = True  # Set to True to use input.txt instead of the example

    example_input = """
    7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3
    """
    
    lines = []
    if use_file_input:
        input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
        if os.path.exists(input_path):
            with open(input_path, 'r') as f:
                lines = f.readlines()
        else:
            print("input.txt not found, using example input.")
            lines = example_input.strip().split('\n')
    else:
        lines = example_input.strip().split('\n')

    # --- Parsing ---
    coords = set()
    max_x, max_y = 0, 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            x_str, y_str = line.split(',')
            x, y = int(x_str), int(y_str)
            coords.add((x, y))
            if x > max_x: max_x = x
            if y > max_y: max_y = y
        except ValueError:
            print(f"Warning: Could not parse line '{line}'")
            continue
    
    if len(coords) < 2:
        print("Need at least two points to form a rectangle.")
        return

    # --- Find largest rectangle ---
    max_area = -1
    largest_rect_points = None
    
    for p1, p2 in itertools.combinations(coords, 2):
        width = abs(p1[0] - p2[0]) + 1
        height = abs(p1[1] - p2[1]) + 1
        area = width * height
        
        if area > max_area:
            max_area = area
            largest_rect_points = (p1, p2)

    p1, p2 = largest_rect_points
    print(f"{p1} and {p2} create a rectangle with area {max_area}")

    if not use_file_input:
        # --- Grid Creation and Printing ---
        grid_width = max_x + 2
        grid_height = max_y + 2
        grid = [['.' for _ in range(grid_width)] for _ in range(grid_height)]
        
        # Mark the rectangle boundary
        start_x, end_x = min(p1[0], p2[0]), max(p1[0], p2[0])
        start_y, end_y = min(p1[1], p2[1]), max(p1[1], p2[1])
        
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if y == start_y or y == end_y or x == start_x or x == end_x:
                    if grid[y][x] == '.':
                        grid[y][x] = '0'

        # Mark the original points
        for x, y in coords:
            grid[y][x] = '#'

        print("\nGrid with largest rectangle:")
        for row in grid:
            print("".join(row))

def solve_b():
    """
    Solves Part B of the Advent of Code 2025 Day 9 puzzle.
    More space-efficient and correct implementation.
    """
    
    # --- Input Handling ---
    use_file_input = True  # Set to True to use input.txt instead of the example

    example_input = """
    7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3
    """
    
    lines = []
    if use_file_input:
        input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
        if os.path.exists(input_path):
            with open(input_path, 'r') as f:
                lines = f.readlines()
        else:
            print("input.txt not found, using example input.")
            lines = example_input.strip().split('\n')
    else:
        lines = example_input.strip().split('\n')

    # --- Parsing ---
    coords_list = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            x_str, y_str = line.split(',')
            x, y = int(x_str), int(y_str)
            coords_list.append((x, y))
        except ValueError:
            print(f"Warning: Could not parse line '{line}'")
            continue
    
    if len(coords_list) < 2:
        print("Need at least two points.")
        return

    segments = []
    for i in range(len(coords_list)):
        p1 = coords_list[i]
        p2 = coords_list[(i + 1) % len(coords_list)]
        segments.append((p1, p2))

    def is_on_boundary(px, py):
        for p1, p2 in segments:
            x1, y1 = p1
            x2, y2 = p2
            if x1 == x2 == px and min(y1, y2) <= py <= max(y1, y2):
                return True
            if y1 == y2 == py and min(x1, x2) <= px <= max(x1, x2):
                return True
        return False

    memo_inside = {}
    def is_inside(px, py):
        if (px, py) in memo_inside:
            return memo_inside[(px, py)]

        if is_on_boundary(px, py):
            memo_inside[(px,py)] = True
            return True
        
        crossings = 0
        for p1, p2 in segments:
            x1, y1 = p1
            x2, y2 = p2
            
            if y1 == y2: continue
            if py < min(y1, y2) or py >= max(y1, y2): continue

            # Edge is to the right of point
            if x1 > px and x2 > px:
                crossings += 1
            # Edge crosses the vertical line at px
            elif (x1 > px and x2 <= px) or (x2 > px and x1 <= px):
                # Calculate intersection point
                x_intersection = (py - y1) * (x2 - x1) / (y2 - y1) + x1
                if x_intersection > px:
                    crossings += 1

        res = crossings % 2 == 1
        memo_inside[(px,py)] = res
        return res

    max_area = 0
    for p1, p2 in itertools.combinations(coords_list, 2):
        x_start, x_end = min(p1[0], p2[0]), max(p1[0], p2[0])
        y_start, y_end = min(p1[1], p2[1]), max(p1[1], p2[1])

        corners = [(x_start, y_start), (x_start, y_end), (x_end, y_start), (x_end, y_end)]
        if not all(is_inside(cx, cy) for cx, cy in corners):
            continue

        has_boundary_crossing = False
        for seg_p1, seg_p2 in segments:
            sx1, sy1 = seg_p1
            sx2, sy2 = seg_p2
            
            # vertical segment
            if sx1 == sx2:
                if x_start < sx1 < x_end and max(y_start, min(sy1, sy2)) < min(y_end, max(sy1, sy2)):
                    has_boundary_crossing = True
                    break
            # horizontal segment
            else:
                if y_start < sy1 < y_end and max(x_start, min(sx1, sx2)) < min(x_end, max(sx1, sx2)):
                    has_boundary_crossing = True
                    break
        
        if has_boundary_crossing:
            continue

        area = (x_end - x_start + 1) * (y_end - y_start + 1)
        max_area = max(max_area, area)
                
    print(f"Largest rectangle between two '#'s avoiding '.' is {max_area}")

solve_a()
solve_b()