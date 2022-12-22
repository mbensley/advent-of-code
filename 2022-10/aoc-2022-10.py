class Display(object):

  def __init__(self, line_count):
    self.x = 1
    self.cycle = 1
    self.lines = ["" for _ in range(line_count)]

  def noop(self):
    self.tick()

  def addx(self, x):
    self.tick()
    self.tick()
    self.x += x

  def tick(self):
    self.add_pixel()
    self.cycle += 1

  def add_pixel(self):
    row = (self.cycle - 1) // 40
    hloc = self.x
    chr = '.'
    scan_loc = (self.cycle - 1) % 40
    if scan_loc in [hloc - 1, hloc, hloc + 1]:
      chr = '#'
    self.lines[row] += chr

  def print_image(self):
    str = ''
    for line in self.lines:
      str += '%s\n' % line
    return str


def main():
  with open('input.txt') as f:
    display = Display(line_count=6)
    command_list = [c.strip().split(' ') for c in f.readlines()]
    for command in command_list:
      # noop
      if len(command) == 1:
        display.noop()
      # addx x
      else:
        display.addx(int(command[1]))
    print(display.print_image())


def main_a():
  with open('input.txt') as f:
    command_list = [c.strip().split(' ') for c in f.readlines()]
    x = 1
    cycle = 0
    signal_sum = 0
    checkpoints = [20, 60, 100, 140, 180, 220]
    for command in command_list:
      # noop
      if len(command) == 1:
        cycle += 1
        if cycle in checkpoints:
          print('next sum [%i]: %i' % (cycle, cycle * x))
          signal_sum += cycle * x
      # addx X
      if len(command) == 2:
        cycle += 2
        if cycle in checkpoints:
          print('next sum [%i]: %i' % (cycle, cycle * x))
          signal_sum += cycle * x
        if cycle - 1 in checkpoints:
          print('next sum [%i]: %i' % (cycle, (cycle - 1) * x))
          signal_sum += (cycle - 1) * x
        x += int(command[1])
    print(signal_sum)

main_a()
main()
