# Timings: Part A: 4:00 / Part B: 6:30
import os

test, no_file = False, False
filename = '2015/%s' % ('input-02.txt' if test else 'input.txt')
test_input = ['2x3x4', '1x1x10']
with open(os.getcwd() + '/advent-of-code/' + filename) as f:
    input = test_input if test and no_file else f.read().splitlines()
    t, t2 = 0, 0
    for line in input:
       # A
        a, b, c = line.split('x')
        a, b, c = int(a), int(b), int(c)
        ab = a*b
        bc = b*c
        ac = a*c
        slack = min(ab, bc, ac)
        t += 2*ab+2*bc+2*ac+slack

        # B
        vol = a*b*c
        p1 = 2*a + 2*b
        p2 = 2*a + 2*c
        p3 = 2*c + 2*b
        r = min(p1, p2, p3)
        t2 += r + vol

    print('Part A: %i' % t)
    print('Part B: %i' % t2)
