import os

L, D, W = 0, 3, 6
A, B, C = 1, 2, 3  # R,P,S
score_dict = {'A': A, 'X': A, 'B': B, 'Y': B, 'C': C, 'Z': C}
r_dict = {'A': {'X': D, 'Y': W, 'Z': L},
          'B': {'X': L, 'Y': D, 'Z': W},
          'C': {'X': W, 'Y': L, 'Z': D}}

#           Lose        Draw        Win
r2_dict = {'A X': C+L, 'A Y': A+D, 'A Z': B+W,
           'B X': A+L, 'B Y': B+D, 'B Z': C+W,
           'C X': B+L, 'C Y': C+D, 'C Z': A+W}


def calc_round1(pair):
    p0, p1 = pair.split()
    return r_dict[p0][p1] + score_dict[p1]


with open(os.getcwd() + '/2022-02/input-t.txt') as f:
    pairs = f.read().splitlines()
    print('Part A: %i' % sum(map(calc_round1, pairs)))
    print('Part B: %i' % sum(map(lambda p: r2_dict[p], pairs)))
