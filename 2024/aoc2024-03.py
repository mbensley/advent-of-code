import os
import re

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))']
    test_input = ['xmul(2,4)&mul[3,7]!^don\'t()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))']
    return test_input if test else f.read().splitlines()


def sum_mult(input, enable_dos):
    def calc_mul(x,y):
        return int(x)*int(y)
    total = 0
    enabled = True
    for line in input:
        for token in re.finditer('mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)', line):
            if token.group(0) == 'do()':
                enabled = True
            elif token.group(0) == 'don\'t()':
                if enable_dos:
                    enabled = False
            else:
                if enabled:
                    total += calc_mul(token.group(1), token.group(2))
    return total

with open(inputfile()) as f:
    input = getinput(f)
    print('Part A: %i' % sum_mult(input, enable_dos=False))
    print('Part B: %i' % sum_mult(input, enable_dos=True))
