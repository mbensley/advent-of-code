import os
from typing import TextIO

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f: TextIO, test: bool = True) -> list[str]:
    test_input = ['987654321111111', '811111111111119']
    return test_input if test else f.read().splitlines()

# Select N digits to get maximum value
def get_max_joltage(bank: str, digits: int) -> list[str]:
    if digits == 1:
        return [str(max(int(x) for x in bank))]
    tens = max(int(x) for x in bank[:1+(-1*digits)])
    tens_index = bank.index(str(tens))
    l = [str(tens)]
    l.extend(get_max_joltage(bank[tens_index+1:], digits-1))
    return l

with open(inputfile()) as f:
    input = getinput(f)
    joltage_sum_a = 0
    joltage_sum_b = 0
    for bank in input:
        joltage_sum_a += int(''.join(get_max_joltage(bank, 2)))
        joltage_sum_b += int(''.join(get_max_joltage(bank, 12)))

    print('Part A: %i' % joltage_sum_a)
    print('Part B: %i' % joltage_sum_b)
