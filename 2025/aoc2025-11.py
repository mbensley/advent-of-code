
import argparse
import os
from collections import defaultdict

def parse_input(lines):
    """
    Parses the input lines into a directed graph.
    'aaa: you hhh' means edges from 'aaa' to 'you' and 'aaa' to 'hhh'.
    """
    graph = defaultdict(list)
    for line in lines:
        if not line.strip():
            continue
        source, destinations = line.split(':', 1)
        source = source.strip()
        destinations = destinations.strip().split()
        for dest in destinations:
            graph[source].append(dest)
    return graph

def visualize_graph(graph):
    """Prints a visualization of the graph."""
    print("Graph visualization:")
    for source, destinations in graph.items():
        print(f"  {source} -> {', '.join(destinations)}")

def solve_a(graph, is_example_a=False):
    """
    Solves part A of the puzzle by finding all unique paths from 'you' to 'out'.
    """
    start_node = 'you'
    end_node = 'out'
    
    paths = []
    
    def find_paths_dfs(current_node, current_path, current_path_set):
        """Recursively finds all paths using DFS."""
        current_path.append(current_node)
        current_path_set.add(current_node)
        
        if current_node == end_node:
            paths.append(list(current_path))
        else:
            # Using list(graph.get(current_node, [])) to handle nodes with no outgoing edges
            for neighbor in graph.get(current_node, []):
                if neighbor not in current_path_set: # Avoid cycles
                    find_paths_dfs(neighbor, current_path, current_path_set)
        
        current_path.pop()
        current_path_set.remove(current_node)

    find_paths_dfs(start_node, [], set())

    if is_example_a:
        print("\nCalculated paths for Part A:")
        for path in paths:
            print(f"  {' -> '.join(path)}")

    return len(paths)

def solve_b(graph, is_example_b=False):
    """
    Solves part B. Checks if the graph is a DAG and uses a DP approach if so.
    """
    all_nodes = sorted(list(set(graph.keys()) | {n for v in graph.values() for n in v}))
    
    # --- DAG Check and Topological Sort ---
    visiting = set()
    visited = set()
    topo_order = []
    has_cycle = False

    def visit(node):
        nonlocal has_cycle
        visiting.add(node)
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in visiting:
                has_cycle = True
                return
            if neighbor not in visited:
                visit(neighbor)
        visiting.remove(node)
        topo_order.append(node)

    for node in all_nodes:
        if node not in visited:
            visit(node)
            if has_cycle:
                break
    
    if has_cycle:
        print("\nError: Graph has a cycle, this algorithm is not applicable for non-DAGs.")
        return -1

    topo_order.reverse()
    
    # --- Path counting on DAG ---
    memo_path_counts = {}
    def count_paths_dag(start_node, end_node, forbidden_nodes=frozenset()):
        state = (start_node, end_node, forbidden_nodes)
        if state in memo_path_counts:
            return memo_path_counts[state]

        dp = defaultdict(int)
        dp[start_node] = 1
        
        for node in topo_order:
            if node == start_node or dp[node] > 0:
                if node in forbidden_nodes:
                    dp[node] = 0
                    continue
                for neighbor in graph.get(node, []):
                     if neighbor not in forbidden_nodes:
                        dp[neighbor] += dp[node]
        
        # The above loop is not quite right for simple paths.
        # Let's count paths from start_node to all other nodes.
        dp = defaultdict(int)
        try:
            start_index = topo_order.index(start_node)
        except ValueError:
            return 0 # start_node not in topo_order (e.g. not in graph)

        dp[start_node] = 1
        for i in range(start_index, len(topo_order)):
            u = topo_order[i]
            if u in forbidden_nodes: continue
            for v in graph.get(u,[]):
                if v not in forbidden_nodes:
                    dp[v] += dp[u]
        
        result = dp[end_node]
        memo_path_counts[state] = result
        return result

    # Case 1: svr -> ... -> dac -> ... -> fft -> ... -> out
    c_svr_dac = count_paths_dag('svr', 'dac', frozenset(['fft']))
    c_dac_fft = count_paths_dag('dac', 'fft', frozenset())
    c_fft_out = count_paths_dag('fft', 'out', frozenset(['dac']))
    case1_paths = c_svr_dac * c_dac_fft * c_fft_out
    
    # Case 2: svr -> ... -> fft -> ... -> dac -> ... -> out
    c_svr_fft = count_paths_dag('svr', 'fft', frozenset(['dac']))
    c_fft_dac = count_paths_dag('fft', 'dac', frozenset())
    c_dac_out = count_paths_dag('dac', 'out', frozenset(['fft']))
    case2_paths = c_svr_fft * c_fft_dac * c_dac_out

    return case1_paths + case2_paths

def main():
    """
    Main function to read input, parse it, and run the solver.
    """
    parser = argparse.ArgumentParser(description="Advent of Code 2025 Day 11")
    parser.add_argument('--example-a', action='store_true', help="Use Example A input")
    parser.add_argument('--example-b', action='store_true', help="Use Example B input")
    args = parser.parse_args()

    lines = []
    is_example_a = args.example_a
    is_example_b = args.example_b

    if is_example_a:
        print("--- Running with Example A data ---")
        lines = [
            "aaa: you hhh",
            "you: bbb ccc",
            "bbb: ddd eee",
            "ccc: ddd eee fff",
            "ddd: ggg",
            "eee: out",
            "fff: out",
            "ggg: out",
            "hhh: ccc fff iii",
            "iii: out",
        ]
    elif is_example_b:
        print("--- Running with Example B data ---")
        lines = [
            "svr: aaa bbb",
            "aaa: fft",
            "fft: ccc",
            "bbb: tty",
            "tty: ccc",
            "ccc: ddd eee",
            "ddd: hub",
            "hub: fff",
            "eee: dac",
            "dac: fff",
            "fff: ggg hhh",
            "ggg: out",
            "hhh: out",
        ]
    else:
        print("--- Running with input.txt ---")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(script_dir, 'input.txt')
        try:
            with open(input_path) as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            print(f"Error: '{input_path}' not found.")
            return

    graph = parse_input(lines)

    if is_example_a or is_example_b:
        visualize_graph(graph)
    
    # --- Part A Solution ---
    result_a = solve_a(graph, is_example_a=is_example_a)
    print(f"\nSolution to Part A (total unique paths): {result_a}")

    # --- Part B Solution ---
    result_b = solve_b(graph, is_example_b=is_example_b)
    print(f"Solution to Part B: {result_b}")

if __name__ == '__main__':
    main()
