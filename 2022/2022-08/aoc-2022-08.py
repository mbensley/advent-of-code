# tree heights 0-9
# visible if trees are strictly shorter in front of it (u/d/l/r)
# 30373
# 25512
# 65332
# 33549
# 35390

#returns a pair of 2x2 matrices
def build_matrices(input):
  tree_grid = []
  visibility_grid = []
  for line in input:
    tree_list = list(line.strip())
    visibility_grid.append([0 for _ in tree_list])
    tree_grid.append([int(x) for x in tree_list])
  return (tree_grid, visibility_grid)


def flood_right(t_grid, v_grid, ri):
  max_height = -1
  for ci in range(len(t_grid[0])):
    cur_height = t_grid[ri][ci]
    if ci == 0:
      v_grid[ri][ci] = 1
      max_height = cur_height
    else:
      if cur_height > max_height:
        v_grid[ri][ci] = 1
        max_height = cur_height


def flood_left(t_grid, v_grid, ri):
  max_height = -1
  for ci in range(len(t_grid[0]) - 1, 0, -1):
    cur_height = t_grid[ri][ci]
    if ci == len(t_grid[0]) - 1:
      v_grid[ri][ci] = 1
      max_height = cur_height
    else:
      if cur_height > max_height:
        v_grid[ri][ci] = 1
        max_height = cur_height


def flood_down(t_grid, v_grid, ci):
  max_height = -1
  for ri in range(len(t_grid)):
    cur_height = t_grid[ri][ci]
    if ri == 0:
      v_grid[ri][ci] = 1
      max_height = cur_height
    else:
      if cur_height > max_height:
        v_grid[ri][ci] = 1
        max_height = cur_height


def flood_up(t_grid, v_grid, ci):
  max_height = -1
  for ri in range(len(t_grid) - 1, 0, -1):
    cur_height = t_grid[ri][ci]
    if ri == len(t_grid) - 1:
      v_grid[ri][ci] = 1
      max_height = cur_height
    else:
      if cur_height > max_height:
        v_grid[ri][ci] = 1
        max_height = cur_height

def calculate_visibility(t_grid, v_grid):
  # calculate visibility for each direction
  for ri in range(len(t_grid[0])):
    flood_right(t_grid, v_grid, ri)
    flood_left(t_grid, v_grid, ri)
  for ci in range(len(t_grid)):
    flood_up(t_grid, v_grid, ci)
    flood_down(t_grid, v_grid, ci)
  return sum([sum(row) for row in v_grid])

def calculate_tree_count(t_grid):
  max_count = 0
  for ri in range(len(t_grid[0])):
    for ci in range(len(t_grid)):
      max_count = max(max_count, count_trees(t_grid, ri, ci))
  return max_count

# from index 0 count everything you can see to the right
def count_row(row):
  if len(row) == 1:
    return 0
  start_height = row[0]
  count = 0
  for height in row[1:]:
    if height >= start_height:
      return count +1
    count += 1
  return count

def count_right(t_grid, ri, ci):
  return count_row(t_grid[ri][ci:])

def count_left(t_grid, ri, ci):
  revrow = t_grid[ri][0:ci+1]
  revrow.reverse()
  return count_row(revrow)

def count_down(t_grid, ri, ci):
  row = [t_grid[xri][ci] for xri in range(ri, len(t_grid[ri]), 1)]
  return count_row(row)

def count_up(t_grid, ri, ci):
  row = [t_grid[xri][ci] for xri in range(ri+1)]
  row.reverse()
  return count_row(row)

def count_trees(t_grid, ri, ci):
  dc = count_down(t_grid, ri, ci)
  lc = count_left(t_grid, ri, ci)
  rc = count_right(t_grid, ri, ci)
  uc = count_up(t_grid, ri, ci)
  return dc*lc*rc*uc

def main():
  with open('input.txt') as f:
    tree_grid, v_grid = build_matrices(list(f))
    print(calculate_visibility(tree_grid, v_grid))
    print(calculate_tree_count(tree_grid))


main()
