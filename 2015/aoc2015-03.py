# Timings: Part A: 4:30 / Part B: 4:00
import os

test, no_file = False, True
filename = '/2015/%s' % ('input-03.txt' if test else 'input.txt')
test_input = '^v^v^v^v^v'
with open(os.getcwd() + '/advent-of-code/' + filename) as f:
    input = test_input if test and no_file else f.read()
    dx = {'^': -1j, 'v': 1j, '>': 1, '<': -1}

    # A
    visited = set()
    pos = complex(0, 0)
    visited.add(pos)
    for c in input:
        pos += dx[c]
        visited.add(pos)

    # B
    visitedB = set()
    posl = [complex(0, 0), complex(0, 0)]
    visitedB.add(posl[0])
    for i, c in enumerate(input):
        pos = posl[i % 2] + dx[c]
        posl[i % 2] = pos
        visitedB.add(pos)

    print('Part A: %i' % len(visited))
    print('Part B: %i' % len(visitedB))
