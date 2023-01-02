import os


def next_d(numa, numb):
    if len(numb) > len(numa):
        numa, numb = numb, numa
    numb = list(reversed(numb))
    for i, d in enumerate(reversed(numa)):
        yield d, numb[i] if i < len(numb) else '0'


def digitadd(a, b, carry):
    def intd(i):
        if i == '=':
            return -2
        if i == '-':
            return -1
        return int(i)

    s = intd(a) + intd(b) + carry
    lookup = {-5: ('0', -1), -4: ('1', -1), -3: ('2', -1), -2: ('=', 0), -1: ('-', 0),
              0: ('0', 0), 1: ('1', 0), 2: ('2', 0), 3: ('=', 1), 4: ('-', 1), 5: ('0', 1)}
    return lookup[s]


def add(numa, numb):
    sum = []
    carry = 0
    for a, b in next_d(numa, numb):
        x, carry = digitadd(a, b, carry)
        sum.append(x)
    if carry:
        sum.append(str(carry))
    sum.reverse()
    return sum


def concat(l: list) -> str:
    output = ''
    for s in l:
        output += s
    return output


def to_dec(l: list) -> int:

    lookup = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
    val = 0
    for i, d in enumerate(reversed(l)):
        val += (5**i) * lookup[d]
    return val


test = False
filename = '/2022-25/input-t.txt' if test else '/2022-25/input.txt'
with open(os.getcwd() + filename) as f:
    sum = []
    for num in f.read().splitlines():
        sum2 = add(sum, num)
        print('[%s] + [%s] = %s' % (concat(sum), concat(num), concat(sum2)))

        print('  [%s] + [%s] = %s' % (to_dec(sum), to_dec(num), to_dec(sum2)))
        if to_dec(sum) + to_dec(num) != to_dec(sum2):
            raise Exception('answer %i is wrong' % to_dec(sum2))
        sum = sum2
    print(concat(sum))
    print(to_dec(sum))
