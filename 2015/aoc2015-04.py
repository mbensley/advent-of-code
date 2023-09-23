# Timings: Part A: 17:30 / Part B: 18:00
import hashlib
import sys

input = 'abcdef'
for next_int in range(sys.maxsize):
    h = hashlib.md5()
    h.update((input + str(next_int)).encode())
    d = h.hexdigest()
    # Part A: '00000'
    # Part B: '000000'
    if d.startswith('00000'):
        print('Answer: %i' % next_int)
        break
