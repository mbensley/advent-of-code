class CrateStacks9000(object):

  def __init__(self):
    self.stacks = []
    self.setup()

  def add_crate(self, index: int, name: str) -> None:
    self.stacks[index - 1].append(name)

  def remove_crate(self, index: int) -> str:
    return self.stacks[index - 1].pop()

  def move(self, count: int, start: int, end: int) -> None:
    for _ in range(count):
      self.add_crate(end, self.remove_crate(start))

  def setup(self) -> None:
    self.setup_real()

  def setup_real(self) -> None:
    self.stacks.append(['S', 'M', 'R', 'N', 'W', 'J', 'V', 'T'])
    self.stacks.append(['B', 'W', 'D', 'J', 'Q', 'P', 'C', 'V'])
    self.stacks.append(['B', 'J', 'F', 'H', 'D', 'R', 'P'])
    self.stacks.append(['F', 'R', 'P', 'B', 'M', 'N', 'D'])
    self.stacks.append(['H', 'V', 'R', 'P', 'T', 'B'])
    self.stacks.append(['C', 'B', 'P', 'T'])
    self.stacks.append(['B', 'J', 'R', 'P', 'L'])
    self.stacks.append(['N', 'C', 'S', 'L', 'T', 'Z', 'B', 'W'])
    self.stacks.append(['L', 'S', 'G'])

  def setup_test(self) -> None:
    self.stacks.append(['Z', 'N'])
    self.stacks.append(['M', 'C', 'D'])
    self.stacks.append(['P'])


class CrateStacks9001(CrateStacks9000):

  def add_crates(self, index: int, names: list) -> None:
    self.stacks[index - 1].extend(names)

  def remove_crates(self, index: int, count: int) -> list:
    removed_stack = []
    for _ in range(count):
      removed_stack.append(self.remove_crate(index))
    removed_stack.reverse()
    return removed_stack

  def move(self, count: int, start: int, end: int) -> None:
    names = self.remove_crates(start, count)
    self.add_crates(end, names)


def parse_and_execute(lines: [str]):
  stacks = CrateStacks9001()
  for line in lines:
    # move 1 from 2 to 1
    elements = line.split(' ')
    count, start, end = int(elements[1]), int(elements[3]), int(elements[5])
    stacks.move(count, start, end)
  return stacks


def main():
  with open('input-full.txt', 'r') as f:
    stacks = parse_and_execute(list(f))
    print(stacks.stacks)
    output_str = ''
    for stack in stacks.stacks:
      output_str += stack[-1]
    print(output_str)


main()