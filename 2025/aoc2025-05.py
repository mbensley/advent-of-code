import os


def solve(data: str) -> int:
    """
    Counts the number of ingredients that fall within any freshness range.

    Args:
        data: A string containing freshness ranges and ingredients,
              separated by a blank line.

    Returns:
        The count of ingredients within the freshness ranges.
    
    Note:
        This code was generated with gemini-2.5-pro without any human intervention.
    """
    sections = data.split('\n\n')
    range_lines = sections[0].split('\n')
    ingredient_lines = sections[1].split('\n')

    freshness_ranges = []
    for line in range_lines:
        if not line:
            continue
        start, end = map(int, line.split('-'))
        freshness_ranges.append((start, end))

    ingredients = [int(line) for line in ingredient_lines if line]

    count = 0
    for ingredient in ingredients:
        for start, end in freshness_ranges:
            if start <= ingredient <= end:
                count += 1
                break
    return count


def count_total_fresh_ingredients(data: str) -> int:
    """
    Calculates the total number of unique freshness values covered by all ranges.

    Args:
        data: A string containing freshness ranges.

    Returns:
        The total count of unique freshness values.

    Note:
        This code was generated with gemini-2.5-pro without any human intervention.
    """
    range_lines = data.split('\n\n')[0].split('\n')

    ranges = []
    for line in range_lines:
        if not line:
            continue
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    if not ranges:
        return 0

    # Sort ranges by the start value
    ranges.sort(key=lambda x: x[0])

    merged_ranges = [ranges[0]]

    for current_start, current_end in ranges[1:]:
        last_start, last_end = merged_ranges[-1]

        if current_start <= last_end:
            # Merge overlapping ranges
            merged_ranges[-1] = (last_start, max(last_end, current_end))
        else:
            # Add new, non-overlapping range
            merged_ranges.append((current_start, current_end))

    total_fresh_ingredients = 0
    for start, end in merged_ranges:
        total_fresh_ingredients += (end - start + 1)

    return total_fresh_ingredients


if __name__ == "__main__":
    # Set to True to use example_data, False to use input.txt
    use_example_data = False

    if use_example_data:
        data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
        print("Using example data")
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(script_dir, 'input.txt')
        with open(input_file, 'r') as f:
            data = f.read()
        print("Using data from input.txt")

    result = solve(data)
    print(f"Number of ingredients within freshness ranges: {result}")
    part2_result = count_total_fresh_ingredients(data)
    print(f"Total number of fresh ingredients: {part2_result}")
