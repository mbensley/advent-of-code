# Timings: Part A: XX:00 / Part B: XX:00
import os
from typing import TextIO
from collections import defaultdict

# https://docs.python.org/3/library/


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = True) -> list[str]:
    test_input = ['125', '17']
    return test_input if test else f.read().splitlines()

# Element Rules
# If the element is 0, it is replaced by an element with value 1.
# If the element has an even number of digits, it is replaced by two stones. The left element value is equal to the left digits. The right element value is equal to the right digits. Remove leading 0s.
# If none of the other rules apply, the element is replaced by a new element equal to the old value * 2024
# Examples:
# [125, 17] returns [253000 1 7]
# [253000 1 7] returns [253 0 2024 14168]
# [0] return [1]
# [299001] returns [299 1]
def blink(stones: list[str]) -> list[str]:
    new_stones: list[str] = []
    for stone in stones:
        n = int(stone)
        if n == 0:
            new_stones.append('1')
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            left = stone[:mid]
            right = stone[mid:]
            new_stones.append(str(int(left)))
            new_stones.append(str(int(right)))
        else:
            new_stones.append(str(n * 2024))
    return new_stones

def blink_large(in_freq: dict[str, int]) -> dict[str, int]:
    stone_freq: dict[str,int] = defaultdict(int)
    for stone, freq in in_freq.items():
        n = int(stone)
        if n == 0:
            stone_freq['1'] = stone_freq['1'] + freq
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            left = stone[:mid]
            right = stone[mid:]
            stone_freq[str(int(left))] = stone_freq[str(int(left))] + freq
            stone_freq[str(int(right))] = stone_freq[str(int(right))] + freq
        else:
            stone_freq[str(n * 2024)] = stone_freq[str(n * 2024)] + freq
    return stone_freq


with open(inputfile()) as f:
    input = getinput(f)
    BLINKS = 6

    print(input)
    in_freq:dict[str,int] = defaultdict(int)
    for stone in input:
        in_freq[stone] = in_freq[stone] + 1
    for _ in range(BLINKS):
        in_freq = blink_large(in_freq)
    total = 0
    for stone, freq in in_freq.items():
        total += freq

    print('Total Elements after %i blinks: %i' % (BLINKS, total))
