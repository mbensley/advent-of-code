# Timings: Part A: XX:00 / Part B: XX:00
from collections import defaultdict
from collections import deque
import ast
import hashlib
import heapq
import math
import os
import queue
import re
import string
import sys
from itertools import product
from itertools import combinations
from functools import cache
from math import floor
from copy import deepcopy
from typing import TextIO
from pprint import pprint

# https://docs.python.org/3/library/

EXAMPLE_INPUT = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".strip().splitlines()

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = False) -> list[str]:
    return EXAMPLE_INPUT if test else f.read().splitlines()

def parse_input(input_lines: list[str]) -> dict[int, tuple[str, list[int]]]:
    # Using a list for mutability, will convert to tuple at the end.
    processed_data = defaultdict(lambda: ['', []])

    for line in input_lines:
        # Using line.split() to handle variable whitespace between items,
        # which correctly groups items into columns based on the example.
        items = line.split()
        for i, item in enumerate(items):
            if item in ('*', '+'):
                processed_data[i][0] = item
            else:
                try:
                    processed_data[i][1].append(int(item))
                except ValueError:
                    # Ignore items that are not numbers or operators
                    pass
    
    # Convert the mutable lists to the desired tuple format and then to a regular dict
    final_data = {k: (v[0], v[1]) for k, v in processed_data.items()}
    return final_data

def parse_input_part_b(input_lines: list[str]) -> dict[int, tuple[str, list[int]]]:
    # This implementation is based on the idea of finding blocks of non-space columns.
    # It then transposes these blocks to read numbers vertically.
    
    if not input_lines:
        return {}

    max_len = max(len(line) for line in input_lines) if input_lines else 0
    padded_lines = [line.ljust(max_len) for line in input_lines]

    # Find columns that are entirely spaces, these are our delimiters.
    space_columns = [all(line[i] == ' ' for line in padded_lines) for i in range(max_len)]
    
    column_groups_indices = []
    current_group = []
    for i in range(max_len):
        if not space_columns[i]:
            current_group.append(i)
        elif current_group:
            column_groups_indices.append(current_group)
            current_group = []
    if current_group:
        column_groups_indices.append(current_group)

    processed_data = defaultdict(lambda: ['', []])
    intermediate_repr = {}

    for i, group_indices in enumerate(column_groups_indices):
        # Extract the block of text for this group from all lines.
        block_of_lines = ["".join(line[j] for j in group_indices) for line in padded_lines]
        
        operator_line_in_block = block_of_lines[-1]
        operator = operator_line_in_block.strip()

        if not operator or operator not in ('*', '+'):
            continue # This group is not a valid operation column.

        number_lines_in_block = block_of_lines[:-1]
        
        # "replace all spaces within a column with xs"
        # I'll interpret this as replacing spaces within the extracted number block.
        padded_number_block = [s.replace(' ', 'x') for s in number_lines_in_block]
        intermediate_repr[i] = padded_number_block

        processed_data[i][0] = operator
        
        if not padded_number_block:
            continue
            
        # To transpose, we need all strings in the block to have the same length.
        max_block_width = max(len(s) for s in padded_number_block) if padded_number_block else 0
        justified_padded_block = [s.ljust(max_block_width, 'x') for s in padded_number_block]

        transposed_block = list(zip(*justified_padded_block))
        
        numbers = []
        for col_chars in transposed_block:
            num_str = "".join(col_chars).replace('x', '')
            if num_str:
                numbers.append(int(num_str))

        processed_data[i][1] = numbers

    print("\nIntermediate representation with 'x' padding for keys 0, 1, and 2:")
    for i in range(3):
        if i in intermediate_repr:
            print(f"Key {i}: {intermediate_repr[i]}")

    final_data = {k: (v[0], v[1]) for k, v in processed_data.items()}
    return final_data

def calculate_part_a(data: dict[int, tuple[str, list[int]]]) -> int:
    total = 0
    for operator, numbers in data.values():
        if not numbers:  # Skip if there are no numbers for a column
            continue
            
        if operator == '*':
            total += math.prod(numbers)
        elif operator == '+':
            total += sum(numbers)
    return total


with open(inputfile()) as f:
    use_part_b_parser = True
    input_lines = getinput(f, test=False)

    if use_part_b_parser:
        data = parse_input_part_b(input_lines)
        print("\nFinal parsed data for keys 0, 1, and 2:")
        for i in range(3):
            if i in data:
                print(f"{i}: {data[i]}")
    else:
        data = parse_input(input_lines)
    
    part_result = calculate_part_a(data)
    
    if use_part_b_parser:
        print('Part B: %i' % part_result)
    else:
        print('Part A: %i' % part_result)
