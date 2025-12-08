import os
import math

# --- Constants ---
NUM_POINTS = 10
NUM_SETS = 3

def _parse_points(input_path):
    """Parses the input file and returns a list of point tuples."""
    points = []
    with open(input_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 3:
            continue
        try:
            points.append((int(parts[0]), int(parts[1]), int(parts[2])))
        except ValueError:
            continue
    return points

def _calculate_distances(points):
    """Calculates all pairwise distances and returns them sorted."""
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]
            distance = math.sqrt(
                (p1[0] - p2[0])**2 +
                (p1[1] - p2[1])**2 +
                (p1[2] - p2[2])**2
            )
            distances.append(((p1, p2), distance))
    
    distances.sort(key=lambda item: item[1])
    return distances

def solve_a():
    """
    Solves Part A of the Advent of Code 2025 Day 8 puzzle.
    """
    print("--- Part A ---")
    input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    points = _parse_points(input_path)
    
    if not points:
        print("No points found in input.")
        return

    distances = _calculate_distances(points)
    
    # Get the top N shortest distances
    top_shortest = distances[:NUM_POINTS]
    
    connection_sets = []
    for pair, dist in top_shortest:
        p1, p2 = pair
        p1_set = None
        p2_set = None

        for s in connection_sets:
            if p1 in s:
                p1_set = s
            if p2 in s:
                p2_set = s
        
        if p1_set is None and p2_set is None:
            connection_sets.append({p1, p2})
        elif p1_set is not None and p2_set is None:
            p1_set.add(p2)
        elif p1_set is None and p2_set is not None:
            p2_set.add(p1)
        elif p1_set is not p2_set:
            p1_set.update(p2_set)
            connection_sets.remove(p2_set)

    if not connection_sets:
        product = 0
    else:
        set_sizes = [len(s) for s in connection_sets]
        set_sizes.sort(reverse=True)
        top_sizes = set_sizes[:NUM_SETS]
        product = math.prod(top_sizes)

    print(f"The product of the sizes of the {NUM_SETS} largest connection sets is: {product}")

def solve_b():
    """
    Solves Part B of the Advent of Code 2025 Day 8 puzzle.
    """
    print("\n--- Part B ---")
    input_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    points = _parse_points(input_path)

    if not points:
        print("No points found in input.")
        return

    distances = _calculate_distances(points)
    
    # Initialize connection sets with each point in its own set
    connection_sets = [{p} for p in points]
    last_connected_pair = None

    for pair_info, dist in distances:
        if len(connection_sets) == 1:
            break

        p1, p2 = pair_info
        p1_set_idx, p2_set_idx = -1, -1

        for i, s in enumerate(connection_sets):
            if p1 in s:
                p1_set_idx = i
            if p2 in s:
                p2_set_idx = i
            if p1_set_idx != -1 and p2_set_idx != -1:
                break
        
        if p1_set_idx != p2_set_idx:
            # Merge the sets
            connection_sets[p1_set_idx].update(connection_sets[p2_set_idx])
            del connection_sets[p2_set_idx]
            last_connected_pair = (p1, p2)

    if last_connected_pair:
        p1, p2 = last_connected_pair
        product = p1[0] * p2[0]
        print(f"Last two points connected: {p1} and {p2}")
        print(f"Product of their X coordinates: {product}")
    else:
        print("Could not determine the final connection.")


solve_a()
solve_b()
