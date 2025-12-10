
import sys
import os
import re

# It's good practice to set a higher recursion limit for deep recursive solutions.
sys.setrecursionlimit(2000)

# Hardcoded example data as requested by the user.
example_data = [
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
]

def solve_recursive(current_state, target_config, diagrams, memo):
    """
    Recursively calculates the minimum steps to reach the target_config.
    It's more self-contained now, relying on arguments rather than globals.
    """
    num_lights = len(target_config)
    if current_state == target_config:
        return 0
    if current_state in memo:
        return memo[current_state]

    # Mark the current state as being visited to prevent infinite recursion
    memo[current_state] = float('inf')
    min_steps = float('inf')

    # Try applying each wiring diagram to the current state
    for diagram in diagrams:
        next_state_list = list(current_state)
        for light_idx in diagram:
            if 0 <= light_idx < num_lights:
                # Toggle the light
                next_state_list[light_idx] = '#' if next_state_list[light_idx] == '.' else '.'
        next_state = "".join(next_state_list)
        
        # Recurse on the new state
        res = solve_recursive(next_state, target_config, diagrams, memo)
        
        # If a solution is found, update the minimum steps
        if res != float('inf'):
            min_steps = min(min_steps, res + 1)

    # Memoize the result for the current state and return it
    memo[current_state] = min_steps
    return min_steps

def main():
    """
    Main function to read input, run the solver for each target, and print results.
    It now uses a unified parsing logic for all input sources.
    """
    USE_EXAMPLE_DATA = False # Set to False to use input.txt
    total_steps = 0
    problem_lines = []

    if USE_EXAMPLE_DATA:
        problem_lines = example_data
        print("--- Running with example_data ---")
    else:
        print("--- Running with input.txt ---")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(script_dir, 'input.txt')
        try:
            with open(input_path) as f:
                problem_lines = f.read().splitlines()
        except FileNotFoundError:
            print(f"Error: '{input_path}' not found.")
            return
        
        if not problem_lines:
            print("Input file is empty.")
            return

    for line in problem_lines:
        if not line.strip(): # Skip empty lines
            continue

        match = re.match(r'\[(.*?)\]\s+(.*?)\s+\{', line)
        if not match:
            print(f"Warning: Skipping malformed line: {line}")
            continue

        t_config = match.group(1)
        diagrams_line = match.group(2)
        
        diagrams_str = diagrams_line.replace('(', '').replace(')', '')
        # Filter out empty strings that can result from splitting
        parts = [part for part in diagrams_str.split() if part]
        diags = [tuple(map(int, part.split(','))) for part in parts]
        
        memo = {}
        num_lights = len(t_config)
        initial_state = '.' * num_lights
        
        result = solve_recursive(initial_state, t_config, diags, memo)
        
        if result == float('inf'):
            print(f"No solution found for '{t_config}'")
        else:
            print(f"Minimum steps for '{t_config}': {result}")
            total_steps += result
            
    print(f"\nSolution to Part A (total steps): {total_steps}")

if __name__ == '__main__':
    main()