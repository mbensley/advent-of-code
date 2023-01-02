import os


def get_next_element_index(index: int, buffer: list):
    for idx, (x, i) in enumerate(buffer):
        if index == i:
            return idx
    return -1
    if False:
        next_idx = 0
        while next_idx < len(buffer)-1:
            print('finding element %i' % next_idx)
            ret_idx = -1
            #    for i in range(len(buffer)):
        #       yield i
            for idx, (x, i) in enumerate(buffer):
                #      yield idx
                if i == next_idx:
                    ret_idx = idx
            next_idx += 1
           # yield ret_idx


def get_element(idx: int, buffer: list) -> int:
    idx_0 = -1  # buffer.index([0, any()])  # % len(buffer)
    for i, (x, j) in enumerate(buffer):
        if x == 0:
            idx_0 = i
    # start searching from 0
    if idx_0 + idx < len(buffer):
        return buffer[idx_0+idx][0]
    new_idx = (idx_0 + idx) % len(buffer)
    return buffer[new_idx][0]


def mix(idx: int, buffer: list):
    # [0, 1, 2, 3] len == 4 so if val % len == 0 then no move
    # 0: no; 1: move to 1
    v = buffer[idx][0]
    new_idx = v + idx
    # print('%i %i %i new_idx: %i' % (v, len(buffer), full_wraps, new_idx))
    # print(new_idx % len(buffer))
    if v > 0:
        if new_idx > len(buffer):  # if wrap need to move an additional N
            new_idx = (new_idx % len(buffer)) + (new_idx // len(buffer))
            new_idx = new_idx % ((len(buffer)-1))
            # print('final new index: %i' % (new_idx % (len(buffer)-1)))
    elif v < 0:
        if new_idx <= 0:  # if wrap need to move an additional N
            new_idx = (len(buffer)-1 - abs(new_idx) % (len(buffer)-1))
    else:
        return
    e = buffer.pop(idx)
    buffer.insert(new_idx, e)


def build_test_buffer(vals: list) -> list:
    return [[x, i] for i, x in enumerate(vals)]


def verify_order(b0: list, b1: list) -> bool:
    for (x, i), (y, j) in zip(b0, b1):
        if x != y:
            return False
    return True


def test_get_element_nowrap():
    val = get_element(0, build_test_buffer([1, 2, -3, 3, -2, 0, 4]))
    if val != 0:
        raise Exception('Expected 0, Actual %i' % val)
    val = get_element(1, build_test_buffer([1, 2, -3, 3, -2, 0, 4]))
    if val != 4:
        raise Exception('Expected 4, Actual %i' % val)
    val = get_element(6, build_test_buffer([0, 1, 2, -3, 3, -2, 4]))
    if val != 4:
        raise Exception('Expected 4, Actual %i' % val)


def test_get_element_wrap():
    val = get_element(2, build_test_buffer([1, 2, -3, 3, -2, 0, 4]))
    if val != 1:
        raise Exception('Expected 1, Actual %i' % val)
    val = get_element(7, build_test_buffer([1, 2, -3, 3, -2, 0, 4]))
    if val != 0:
        raise Exception('Expected 0, Actual %i' % val)
    val = get_element(8, build_test_buffer([1, 2, -3, 3, -2, 0, 4]))
    if val != 4:
        raise Exception('Expected 0, Actual %i' % val)
    val = get_element(7*3, build_test_buffer([1, 2, -3, 3, -2, 0, 4]))
    if val != 0:
        raise Exception('Expected 0, Actual %i' % val)


def test_get_next_element():
    buffer = build_test_buffer([1, 2, -3, 3, -2, 0, 4])

    idx = get_next_element_index(0, buffer)
    if idx != 0:
        raise Exception('Expected %i, Actual: %i' % (0, idx))
    idx = get_next_element_index(1, buffer)
    if idx != 1:
        raise Exception('Expected %i, Actual: %i' % (1, idx))
    idx = get_next_element_index(2, buffer)
    if idx != 2:
        raise Exception('Expected %i, Actual: %i' % (2, idx))


def test_mix_pos_wrap():
    buffer = build_test_buffer((1, 2, -3, 0, 3, 4, -2))
    mix(5, buffer)  # Move 4
    if not verify_order(buffer, build_test_buffer((1, 2, -3, 4, 0, 3, -2))):
        raise Exception('4 should end up between -3 and 0:\n\t%s' % buffer)


def test_mix_pos_wrap_twice():
    buffer = build_test_buffer((1, 2, -3, 0, 10, 4, -2))
    mix(4, buffer)  # Move 4
    if not verify_order(buffer, build_test_buffer((1, 2, 10, -3, 0, 4, -2))):
        raise Exception('10 should end up between 2 and -3:\n\t%s' % buffer)


def test_mix_pos_wrap_n():
    for n in range(1, 100):
        buffer = build_test_buffer((1, 2, -3, 0, 7+(6*n), 4, -2))
        mix(4, buffer)  # Move 6
        if not verify_order(buffer, build_test_buffer((1, 2, -3, 0, 4, 7+(6*n), -2))):
            raise Exception(
                '%i: %i should end up between 0 and 4:\n\t%s' % (n, 7+6*n, buffer))


def test_mix_neg_wrap_n():
    for n in range(0, 100):
        buffer = build_test_buffer((1, 2, -1-(6*n), 0, 7, 4, -2))
        mix(2, buffer)  # Move -1*n
        if not verify_order(buffer, build_test_buffer((1, -1-(6*n), 2, 0, 7, 4, -2))):
            raise Exception(
                '%i: %i should end up between 1 and 2:\n\t%s' % (n, -1-(6*n), buffer))


def test_mix_neg_nwr():
    buffer = build_test_buffer((1, -3, 2, 3, -2, 0, 4))
    mix(4, buffer)  # Move -2
    if not verify_order(buffer, build_test_buffer((1, -3, -2, 2, 3, 0, 4))):
        raise Exception('-2 should end up between -3 and 2:\n\t%s' % buffer)


def test_mix_neg_wrap1():
    buffer = build_test_buffer((1, 2, -2, -3, 0, 3, 4))
    mix(2, buffer)  # Move -2
    if not verify_order(buffer, build_test_buffer((1, 2, -3, 0, 3, 4, -2))):
        raise Exception('-2 should end up between 4 and 1:\n\t%s' % buffer)


def test_mix_neg_wrap2():
    buffer = build_test_buffer((1, -3, 2, 3, -2, 0, 4))
    mix(1, buffer)  # Move -3
    if not verify_order(buffer, build_test_buffer((1, 2, 3, -2, -3, 0, 4))):
        raise Exception('-3 should end up between -2 and 0:\n\t%s' % buffer)


def test_mix_neg_wrap_twice():
    buffer = build_test_buffer((1, -10, 2, 3, -2, 0, 4))
    mix(1, buffer)  # Move -10
    if not verify_order(buffer, build_test_buffer((1, 2, 3, -10, -2, 0, 4))):
        raise Exception('-10 should end up between 3 and -2:\n\t%s' % buffer)


def test_mix_zero():
    buffer = build_test_buffer((1, 2, -3, 0, 3, 4, -2))
    mix(3, buffer)  # Move 0
    if not verify_order(buffer, build_test_buffer((1, 2, -3, 0, 3, 4, -2))):
        raise Exception('0 should not move')


def test_mix_pos_nwr():
    buffer = build_test_buffer((1, 2, -3, 3, -2, 0, 4))
    mix(0, buffer)  # Move 1
    if not verify_order(buffer, build_test_buffer((2, 1, -3, 3, -2, 0, 4))):
        raise Exception('1 should move between 2 and -3:\n\t%s' % buffer)


def test_full_mix():
    buffer = build_test_buffer((1, 2, -3, 3, -2, 0, 4))

    for i in range(len(buffer)):
        idx = get_next_element_index(i, buffer)
        mix(idx, buffer)
      #  idx = next(gen)
    expected_buffer = build_test_buffer((1, 2, -3, 4, 0, 3, -2))
    if not verify_order(buffer, expected_buffer):
        raise Exception('Wrong order:\n\tExpected: %s\n\tActual: %s' %
                        (expected_buffer, buffer))


test_get_next_element()
test_mix_pos_nwr()
test_mix_pos_wrap()
test_mix_pos_wrap_twice()
test_mix_pos_wrap_n()
test_mix_neg_wrap_n()
test_mix_zero()
test_mix_neg_nwr()
test_mix_neg_wrap1()
test_mix_neg_wrap2()
test_mix_neg_wrap_twice()
test_get_element_nowrap()
test_get_element_wrap()
test_full_mix()
with open(os.getcwd() + '/2022-20/input-t.txt') as f:
    buffer_in = [int(x) for x in f.read().splitlines()]
    buffer_a = [[x, i] for i, x in enumerate(buffer_in)]

    # idx = next(gen)
   # while idx is not None:
    for i in range(len(buffer_a)):
        idx = get_next_element_index(i, buffer_a)
        mix(idx, buffer_a)
    esum = 0
    for i in (1000, 2000, 3000):
        esum += get_element(i, buffer_a)
    print('Part A: %i' % esum)

    buffer_b = [[x*811589153, i] for i, x in enumerate(buffer_in)]
    print('Round %i: %s' % (0, buffer_b[0:7]))

    for times in range(10):
        for i in range(len(buffer_b)):
            idx = get_next_element_index(i, buffer_b)
            mix(idx, buffer_b)
        print('Round %i: %s' % (times+1, buffer_b[0:7]))
    esum = 0
    for i in (1000, 2000, 3000):
        esum += get_element(i, buffer_b)
    print('Part B: %i' % esum)
