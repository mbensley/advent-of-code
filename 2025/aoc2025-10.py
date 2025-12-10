import sys
from collections import deque
import os
import re
from datetime import datetime, timedelta

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
    Recursively calculates the minimum steps to reach the target_config for Part A.
    """
    num_lights = len(target_config)
    if current_state == target_config:
        return 0
    if current_state in memo:
        return memo[current_state]

    memo[current_state] = float('inf')
    min_steps = float('inf')

    for diagram in diagrams:
        next_state_list = list(current_state)
        for light_idx in diagram:
            if 0 <= light_idx < num_lights:
                next_state_list[light_idx] = '#' if next_state_list[light_idx] == '.' else '.'
        next_state = "".join(next_state_list)
        
        res = solve_recursive(next_state, target_config, diagrams, memo)
        
        if res != float('inf'):
            min_steps = min(min_steps, res + 1)

    memo[current_state] = min_steps
    return min_steps

try:
    from scipy.optimize import linprog
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    
def _solve_b_fallback(initial_state, target_state, diagrams):
    """
    Fallback solver using the best custom implementation (branch-and-bound)
    in case scipy is not available.
    """
    num_lights = len(initial_state)
    num_diagrams = len(diagrams)
    
    if not any(target_state): return 0
    if not diagrams: return float('inf')

    # --- Pre-processing Step ---
    live_diagrams = [tuple(d) for d in diagrams]
    mutable_target = list(target_state)
    fixed_steps = 0
    
    while True:
        num_live_diagrams = len(live_diagrams)
        if num_live_diagrams == 0: break

        D_live = [[0] * num_live_diagrams for _ in range(num_lights)]
        for i, diag in enumerate(live_diagrams):
            for light_idx in diag:
                if 0 <= light_idx < num_lights:
                    D_live[light_idx][i] += 1
        
        diag_to_lights_map = {}
        for r in range(num_lights):
            non_zero_cols = [c for c in range(num_live_diagrams) if D_live[r][c] > 0]
            if len(non_zero_cols) == 1:
                diag_idx = non_zero_cols[0]
                if diag_idx not in diag_to_lights_map:
                    diag_to_lights_map[diag_idx] = []
                diag_to_lights_map[diag_idx].append(r)

        if not diag_to_lights_map: break

        newly_fixed_indices = set()
        newly_fixed_steps = {}
        
        for diag_idx, light_indices in diag_to_lights_map.items():
            x_val = -1; consistent = True
            for light_idx in light_indices:
                coeff, target_val = D_live[light_idx][diag_idx], mutable_target[light_idx]
                if coeff == 0: continue
                if target_val < 0 or target_val % coeff != 0:
                    consistent = False; break
                val = target_val // coeff
                if x_val == -1: x_val = val
                elif x_val != val: consistent = False; break
            
            if consistent and x_val != -1:
                for r in range(num_lights):
                    if r not in light_indices and mutable_target[r] < x_val * D_live[r][diag_idx]:
                        consistent = False; break
                if consistent:
                    newly_fixed_indices.add(diag_idx)
                    newly_fixed_steps[diag_idx] = x_val
        
        if not newly_fixed_indices: break

        for diag_idx in sorted(list(newly_fixed_indices), reverse=True):
            steps = newly_fixed_steps[diag_idx]
            fixed_steps += steps
            for light_idx in live_diagrams[diag_idx]:
                 if 0 <= light_idx < len(mutable_target):
                    mutable_target[light_idx] -= steps
            del live_diagrams[diag_idx]
        
        if any(v < 0 for v in mutable_target): return float('inf')

    # --- Main DP on Reduced Problem ---
    target_state = tuple(mutable_target)
    diagrams = live_diagrams
    num_diagrams = len(diagrams)
    
    if not any(target_state): return fixed_steps
    if not diagrams: return float('inf')

    D_orig = [[0] * num_diagrams for _ in range(num_lights)]
    for i, diag in enumerate(diagrams):
        for light_idx in diag:
            if 0 <= light_idx < num_lights:
                D_orig[light_idx][i] += 1
    
    diag_info = []
    for i in range(num_diagrams):
        upper_bound = float('inf'); has_effect = False
        for r in range(num_lights):
            if D_orig[r][i] > 0:
                has_effect = True
                upper_bound = min(upper_bound, target_state[r] // D_orig[r][i])
        if not has_effect: upper_bound = float('inf')
        diag_info.append({'orig_idx': i, 'domain_size': upper_bound})

    diag_info.sort(key=lambda x: x['domain_size'])
    sorted_indices = [info['orig_idx'] for info in diag_info]
    D = [[D_orig[r][c] for c in sorted_indices] for r in range(num_lights)]
    
    memo = {}
    def _solve_dp(diag_idx, current_target):
        if not any(v > 0 for v in current_target): return 0
        if diag_idx == num_diagrams: return float('inf')
        state = (diag_idx, current_target)
        if state in memo: return memo[state]

        min_total_steps = float('inf')
        d_col = [D[i][diag_idx] for i in range(num_lights)]
        if not any(d_col):
            res = _solve_dp(diag_idx + 1, current_target)
            memo[state] = res
            return res

        upper_bound = float('inf')
        for i in range(num_lights):
            if d_col[i] > 0: upper_bound = min(upper_bound, current_target[i] // d_col[i])
        
        for x_val in range(int(upper_bound), -1, -1):
            next_target = tuple(current_target[i] - x_val * d_col[i] for i in range(num_lights))
            sub_res = _solve_dp(diag_idx + 1, next_target)
            if sub_res != float('inf'):
                min_total_steps = min(min_total_steps, x_val + sub_res)

        memo[state] = min_total_steps
        return min_total_steps

    result = _solve_dp(0, target_state)
    return (result + fixed_steps) if result != float('inf') else float('inf')

def solve_b_scipy(initial_state, target_state, diagrams):
    """
    Solves the ILP problem using scipy.optimize.linprog.
    """
    num_lights = len(initial_state)
    num_diagrams = len(diagrams)
    
    if not any(target_state): return 0
    if not diagrams: return float('inf')

    # Formulate as D*x = T
    D = [[0] * num_diagrams for _ in range(num_lights)]
    for i, diag in enumerate(diagrams):
        for light_idx in diag:
            if 0 <= light_idx < num_lights:
                D[light_idx][i] += 1
    
    # c is the objective function: minimize sum(x)
    c = [1] * num_diagrams
    
    # Bounds for x_i are (0, inf)
    bounds = (0, None)
    
    # All variables must be integers
    integrality = [1] * num_diagrams
    
    res = linprog(c, A_eq=D, b_eq=list(target_state), bounds=bounds, integrality=integrality, method='highs')
    
    if res.success:
        return int(round(res.fun))
    else:
        return float('inf')

SCIPY_WARNED = False

def solve_b(initial_state, target_state, diagrams):
    """
    Dispatcher function for Part B. Uses scipy if available, otherwise falls back.
    """
    global SCIPY_WARNED
    if SCIPY_AVAILABLE:
        return solve_b_scipy(initial_state, target_state, diagrams)
    else:
        if not SCIPY_WARNED:
            print("\n---")
            print("Warning: 'scipy' library not found.")
            print("Falling back to a much slower custom solver for Part B.")
            print("For a significant performance increase, please install scipy:")
            print("pip install scipy")
            print("---\n")
            SCIPY_WARNED = True
        return _solve_b_fallback(initial_state, target_state, diagrams)

def main():
    """
    Main function to read input, run solvers for Parts A and B, and print results.
    """
    USE_EXAMPLE_DATA = False # Set to False to use input.txt
    total_steps_a = 0
    total_steps_b = 0
    problem_lines = []
    any_b_solution_failed = False

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

    num_lines = len(problem_lines)
    for i, line in enumerate(problem_lines):
        if not line.strip():
            continue

        # --- Parsing ---
        try:
            part1, part3 = line.split('{')
            part3 = part3.strip().rstrip('}')
            target_voltages = tuple(map(int, part3.split(',')))

            match = re.match(r'\[(.*?)\]\s*(.*)', part1)
            if not match:
                raise ValueError("Could not parse t_config and diagrams")

            t_config = match.group(1)
            diagrams_line = match.group(2).strip()
            
            diagrams_str = diagrams_line.replace('(', '').replace(')', '')
            parts = [part for part in diagrams_str.split() if part]
            diags = [tuple(map(int, p.split(','))) for p in parts if p]

        except (ValueError, IndexError):
            print(f"Warning: Skipping malformed line: {line}")
            continue
        
        print(f"\nProcessing line {i+1}/{num_lines}: '{line[:40]}...'")

        # --- Part A Solution ---
        memo_a = {}
        initial_state_a = '.' * len(t_config)
        result_a = solve_recursive(initial_state_a, t_config, diags, memo_a)
        
        if result_a == float('inf'):
            print(f"  Part A - No solution found for '{t_config}'")
        else:
            print(f"  Part A - Minimum steps for '{t_config}': {result_a}")
            total_steps_a += result_a

        # --- Part B Solution ---
        initial_state_b = (0,) * len(target_voltages)
        result_b = solve_b(initial_state_b, target_voltages, diags)

        if result_b == float('inf'):
            print(f"  Part B - No solution found for {target_voltages}")
            any_b_solution_failed = True
        else:
            print(f"  Part B - Minimum steps for {target_voltages}: {result_b}")
            total_steps_b += result_b
            
    print(f"\nSolution to Part A (total steps): {total_steps_a}")
    print(f"Solution to Part B (total steps): {total_steps_b}")

    if any_b_solution_failed:
        print("\nNote: A solution for Part B could not be found for one or more rows.")

if __name__ == '__main__':
    main()