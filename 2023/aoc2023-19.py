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

# https://docs.python.org/3/library/


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input-s.txt')

def getinput(f, test=False):
    test_input = ['2x3x4', '1x1x10']
    return test_input if test else f.read()

def build_workflows(input):
    w = {}
    for line in input.splitlines():
        label, r = line.split('{')
        r = r[:-1]
        rules = []
        for rule in r.split(','):
            rules.append(rule)
        w[label] = rules
    return w

def build_parts(input):
    parts = []
    for line in input.splitlines():
        l = line[1:-1]
        part = {}
        for tk in l.split(','):
            label, val = tk.split('=')
            part[label] = int(val)
        parts.append(part)
    return parts

def calc(part, workflows, start):
    workflow = workflows[start]
    while True:
        for test in workflow:
            if test == 'A': return True
            if test == 'R': return False
            if ':' not in test:
                return calc(part, workflows, test)
            rule, next_label = test.split(':')
            if '>' in rule:
                sym = '>'
                prop, target = rule.split('>')
                if part[prop] > int(target):
                    if next_label == 'A': return True
                    if next_label == 'R': return False
                    return calc(part, workflows, next_label)
            if '<' in rule:
                sym = '<'
                prop, target = rule.split('<')
                if part[prop] < int(target):
                    if next_label == 'A': return True
                    if next_label == 'R': return False
                    return calc(part, workflows, next_label)

def calc_combinations(workflows, start, minmaxdict):
    def c(values):
        cs = 1
        for value in values:
            cs *= (value[1] - value[0])
        return cs
    total = 0
    for test in workflows[start]:
        print(test)
        if test == 'A':
            total += c(minmaxdict.values())
            break
        if test == 'R': return 0
        if ':' not in test:
            total += calc_combinations(workflows, test, minmaxdict.copy())
            continue
        rule, next_label = test.split(':')
        if '>' in rule:
            prop, target = rule.split('>')
            newdict = minmaxdict.copy()
            tmin,tmax = newdict[prop]
            if int(target) > tmax: continue
            if int(target) > tmin: newdict[prop][0] = int(target)
            if next_label == 'A':
                total += c(newdict.values())
                continue
            if next_label == 'R': continue
            
            total += calc_combinations(workflows, next_label, newdict)
        if '<' in rule:
            prop, target = rule.split('<')
            newdict = minmaxdict.copy()
            tmin,tmax = newdict[prop]
            if int(target) < tmin: continue
            if int(target) > tmax: newdict[prop][0] = int(target)
            if next_label == 'A':
                total += c(newdict.values())
                continue
            if next_label == 'R': continue
            total += calc_combinations(workflows, next_label, newdict)
    return total

with open(inputfile()) as f:
    input = getinput(f)
    w, p = input.split('\n\n')
    parts = build_parts(p)
    workflows = build_workflows(w)
    tot_ratings = 0
    for part in parts:
        if calc(part, workflows, 'in'):
            tot_ratings += sum(part.values())


    print('Part A: %i' % tot_ratings)
    
    def get_range(prop):
        return 
    print('Part B: %i' % calc_combinations(workflows, 'in',
                                           {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's':[1, 4000]}))
