# Timings: Part A: 6:00 / Part B: 15:45
import os


def inputfile():
    year_dir = '2015'
    filename = os.path.join(year_dir, 'input.txt')
    return os.path.join(os.getcwd(), filename)


def getinput(f, test):
    test_input = ['ugknbfddgicrmopn']
    return test_input if test else f.read().splitlines()


def three_vowels(s):
    v = 'aeiou'
    count = 0
    for c in s:
        if c in v:
            count += 1
        if count >= 3:
            return True
    return False


def aa(s):
    last = ''
    for c in s:
        if c == last:
            return True
        last = c
    return False


def not_contain(s):
    bad = ['ab', 'cd', 'pq', 'xy']
    return not any(b in s for b in bad)


def isnice(s):
    return three_vowels(s) and aa(s) and not_contain(s)


def aabb(s):
    for i in range(len(s)-2):
        head_s = s[i:i+2]
        rem_s = s[i+2:]
        if head_s in rem_s:
            return True
    return False


def xyx(s):
    for i in range(len(s)-2):
        if s[i] == s[i+2]:
            return True
    return False


def isnice_b(s):
    return aabb(s) and xyx(s)


with open(inputfile()) as f:
    input = getinput(f, test=False)

    count_a = 0
    count_b = 0
    for s in input:
        if isnice(s):
            count_a += 1
        if isnice_b(s):
            count_b += 1

    print('Part A: %i' % count_a)
    print('Part B: %i' % count_b)
