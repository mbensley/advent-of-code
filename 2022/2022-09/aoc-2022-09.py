# keep a set of Point locations that the tail has visited
# len(set) == answer

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
UL = 'UL'
UR = 'UR'
DL = 'DL'
DR = 'DR'


class RopeGrid(object):

  def __init__(self, num_knots):
    self.knots = [[0, 0] for _ in range(num_knots)]
    self.tail_locations = set([(0, 0)])

  def move_knot(self, dir, index):
    knot = self.knots[index]
    #print("Updating %i %s" % (index, dir))
    #print(self.knots[index])
    if dir == UP:
      self.knots[index][1] = self.knots[index][1] + 1
    if dir == UR:
      self.knots[index][1] = self.knots[index][1] + 1
      self.knots[index][0] = self.knots[index][0] + 1
    if dir == UL:
      self.knots[index][1] = self.knots[index][1] + 1
      self.knots[index][0] = self.knots[index][0] - 1
    if dir == DOWN:
      self.knots[index][1] = self.knots[index][1] - 1
    if dir == DL:
      self.knots[index][1] = self.knots[index][1] - 1
      self.knots[index][0] = self.knots[index][0] - 1
    if dir == DR:
      self.knots[index][1] = self.knots[index][1] - 1
      self.knots[index][0] = self.knots[index][0] + 1
    if dir == LEFT:
      self.knots[index][0] = self.knots[index][0] - 1
    if dir == RIGHT:
      self.knots[index][0] = self.knots[index][0] + 1

  # print(self.knots[index])
  #print(self.knots)
    self.print_move(dir, index)

  def add_tail_location(self):
    self.tail_locations.add((self.knots[-1][0], self.knots[-1][1]))

  def print_move(self, dir, index):
    #print("Moving %s to %s" % (dir, str(self.knots[index])))
    #print("Moving %s" % dir)
    pass

  def has_knot(self, x, y):
    for i, (kx, ky) in enumerate(self.knots):
      if x == kx and y == ky:
        if i == 0:
          return 'H'
        return i
    return -1

  def get_grid_lines(self):
    min_x = min(map(lambda k: k[0], self.knots))
    min_y = min(map(lambda k: k[1], self.knots))
    max_x = max(map(lambda k: k[0], self.knots))
    max_y = max(map(lambda k: k[1], self.knots))
    lines = []
    for y in range(min(0, min_y), max_y + 2, 1):
      line = ''
      for x in range(min(0, min_x), max_x + 2, 1):
        knot_index = self.has_knot(x, y)
        if knot_index != -1:
          line += str(knot_index)
        else:
          line += '.'
      lines.append(line)
    lines.reverse()
    return lines

  def __str__(self):
    str = ''
    for line in self.get_grid_lines():
      str += '%s\n' % line
    return str

  def update_grid(self, dir):
    next_dir = dir
    for index in range(len(self.knots) - 1):
      #print("index %i" % index)
      head_knot = self.knots[index]
      tail_knot = self.knots[index + 1]
      prev_head_knot = (head_knot[0], head_knot[1])
      self.move_knot(next_dir, index)
      next_dir = self.get_next_dir(next_dir, prev_head_knot, head_knot,
                                   tail_knot)
      if not next_dir:
        print("not moving, return")
        return
    print("moving tail")
    self.move_knot(next_dir, len(self.knots) - 1)
    self.add_tail_location()
    #next_dir = self.update_grid_helper(next_dir, index, index+1)

  def get_next_dir(self, dir, prev_head_knot, head_knot, tail_knot):
    # 9 possible locations for a tail
    # ...
    # .H.
    # ...
    # for each direction there are 3 categories to consider
    if dir == UP:
      # .N.
      # .H.
      # XXX
      if prev_head_knot[1] > tail_knot[1]:
        if prev_head_knot[0] == tail_knot[0]:
          return UP
        if prev_head_knot[0] < tail_knot[0]:
          return UL
        return UR
    elif dir == UR:
      # X.N
      # XH.
      # XXX
      if prev_head_knot[1] > tail_knot[1]:
        if prev_head_knot[0] < tail_knot[0]:
          return UP
        if prev_head_knot[0] == tail_knot[0]:
          return UR
        return UR
      if prev_head_knot[1] == tail_knot[1] and prev_head_knot[0] > tail_knot[0]:
        return UR
      if prev_head_knot[1] < tail_knot[1] and prev_head_knot[0] > tail_knot[0]:
        return RIGHT
    elif dir == UL:
      # N.X
      # .HX
      # XXX
      # NEXT TO FIX
      if prev_head_knot[1] > tail_knot[1]:
        if prev_head_knot[0] < tail_knot[0]:
          return UL
        if prev_head_knot[0] == tail_knot[0]:
          return UL
        return UP
      if prev_head_knot[1] == tail_knot[1] and prev_head_knot[0] < tail_knot[0]:
        return UL
      if prev_head_knot[1] < tail_knot[1] and prev_head_knot[0] < tail_knot[0]:
        return LEFT
    elif dir == DOWN:
      # XXX
      # .H.
      # .N.
      if prev_head_knot[1] < tail_knot[1]:
        if prev_head_knot[0] == tail_knot[0]:
          return DOWN
        if prev_head_knot[0] < tail_knot[0]:
          return DL
        return DR
    elif dir == DL:
      # XXX
      # .HX
      # N.X
      if prev_head_knot[1] < tail_knot[1]:
        if prev_head_knot[0] > tail_knot[0]:
          return DOWN
        return DL
      if prev_head_knot[1] == tail_knot[1] and prev_head_knot[0] < tail_knot[0]:
        return DL
      if prev_head_knot[1] > tail_knot[1] and prev_head_knot[0] < tail_knot[0]:
        return LEFT
    elif dir == DR:
      # XXX
      # XH.
      # X.N
      if prev_head_knot[1] < tail_knot[1]:
        if prev_head_knot[0] < tail_knot[0]:
          return DOWN
        return DR
      if prev_head_knot[1] == tail_knot[1] and prev_head_knot[0] > tail_knot[0]:
        return DR
      if prev_head_knot[1] > tail_knot[1] and prev_head_knot[0] > tail_knot[0]:
        return RIGHT
    elif dir == LEFT:
      # ..X
      # NHX
      # ..X
      if prev_head_knot[0] < tail_knot[0]:
        if prev_head_knot[1] < tail_knot[1]:
          return DL
        if prev_head_knot[1] == tail_knot[1]:
          return LEFT
        return UL
    elif dir == RIGHT:
      # X..
      # XHN
      # X..
      if prev_head_knot[0] > tail_knot[0]:
        if prev_head_knot[1] > tail_knot[1]:
          return UR
        if prev_head_knot[1] < tail_knot[1]:
          return DR
        return RIGHT

    return None


def main():
  #file, num_knots = 'input-test-large.txt', 10
  #file, num_knots = 'input-test-simple.txt', 10
  #file, num_knots = 'input-test.txt', 2
  file, num_knots = 'input.txt', 10

  with open(file) as f:
    grid = RopeGrid(num_knots)
    print(grid)
    for command in f.readlines():
      dir, count = command.strip().split(' ')
      for _ in range(int(count)):
        grid.update_grid(dir)
        print(grid)
        print('')

  #print(grid.knots)
  print(len(grid.tail_locations))


main()