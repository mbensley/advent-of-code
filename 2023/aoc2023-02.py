# Timings: Part A: 3:00 / Part B: 1:30
from collections import defaultdict
from collections import deque
import ast
import hashlib
import heapq
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
    return os.path.join(os.path.dirname(__file__), 'input.txt')


def getinput(f, test=False):
    test_input = ['']
    return test_input if test else f.read().splitlines()

with open(inputfile()) as f:
    input = getinput(f)

    # Part A
    mr,mg,mb = 12, 13, 14
    totala = 0
    for line in input:
      gts, games = line.split(': ')
      gnum = gts.split()[1]
      ok = True
      for game in games.split('; '):
        gr,gg,gb=0,0,0
        tks = game.split(', ')
        for t in tks:
          n,c = t.split()
          if c == 'red':
            gr = int(n)
          if c == 'green':
            gg = int(n)
          if c == 'blue':
            gb = int(n)
        if gr > mr or gg > mg or gb > mb:
          ok = False
      if ok:
        totala += int(gnum)

    # Part B
    totalb = 0
    for line in input:
      gts, games = line.split(': ')
      gnum = gts.split()[1]
      mr,mg,mb=0,0,0
      for game in games.split('; '):
        gr,gg,gb=0,0,0
        tks = game.split(', ')
        for t in tks:
          n,c = t.split()
          n =int(n)
          if c == 'red':
            if n > mr:
              mr = n
          if c == 'green':
            if n > mg:
              mg = n
          if c == 'blue':
            if n > mb:
              mb = n
      totalb += (mr*mb*mg)
    print(totalb)

    print('Part A: %i' % totala)
    print('Part B: %i' % totalb)
