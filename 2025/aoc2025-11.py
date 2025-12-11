
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

def solve_a(graph, is_example=False):
    """
    Solves part A of the puzzle by finding all unique paths from 'you' to 'out'.
    """
    start_node = 'you'
    end_node = 'out'
    
    paths = []
    
    def find_paths_dfs(current_node, current_path):
        """Recursively finds all paths using DFS."""
        current_path.append(current_node)
        
        if current_node == end_node:
            paths.append(list(current_path))
        else:
            # Using list(graph.get(current_node, [])) to handle nodes with no outgoing edges
            for neighbor in graph.get(current_node, []):
                if neighbor not in current_path: # Avoid cycles
                    find_paths_dfs(neighbor, current_path)
        
        current_path.pop()

    find_paths_dfs(start_node, [])

    if is_example:
        print("\nCalculated paths:")
        for path in paths:
            print(f"  {' -> '.join(path)}")

    return len(paths)

def main():
    """
    Main function to read input, parse it, and run the solver.
    """
    is_example = False
    
    if is_example:
        print("--- Running with example data ---")
        example_input = [
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
        lines = example_input
    else:
        print("--- Running with input.txt ---")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(script_dir, 'input.txt')
        try:
            with open(input_path) as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            print(f"Error: '{input_path}' not found. Create the file or use --example.")
            return

    graph = parse_input(lines)

    if is_example:
        visualize_graph(graph)
    
    # --- Part A Solution ---
    result_a = solve_a(graph, is_example=is_example)
    print(f"\nSolution to Part A (total unique paths): {result_a}")

if __name__ == '__main__':
    main()
