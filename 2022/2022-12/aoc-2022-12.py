import string
import queue

def build_heightmap(lines, rotate):
  pointgrid = []
  for line in lines:
    next_row = []
    pointgrid.append(next_row)
    for c in line:
      if c not in ['E', 'S'] and rotate:
        index = string.ascii_lowercase.find(c)
        next_row.append(string.ascii_lowercase[25-index])
      else:
        next_row.append(c)
  return pointgrid

class Point(object):

 def __init__(self, x, y):
  self.x = x
  self.y = y

 def getxy(self):
  return (self.x, self.y)

 def __hash__(self):
  return hash((self.x, self.y))

 def __eq__(self, other):
  return self.x == other.x and self.y == other.y

 def __repr__(self):
  return '(%i,%i)' % (self.x, self.y)


class Vertex(object):

 def __init__(self, point, height):
  self.height = height
  self.neighbors = set()
  self.point = point

 def __hash__(self):
  return hash(self.point)

 def __eq__(self, other):
  return self.point.x == other.point.x and self.point.y == other.point.y

 def __repr__(self):
  neighbor_pts = ['%s[%s]' % (v.point, v.height) for v in self.neighbors]
  return '(%i,%i)[%s]{%s}' % (self.point.x, self.point.y, self.height, str(neighbor_pts))


def find_points(point_char, pointmap):
 points = []
 for y, row in enumerate(pointmap):
  for x, c in enumerate(row):
   if c == point_char:
    points.append(Point(x, y))
 return points

def djikstra(vdict, s_point, e_point, flood):
  def fq(v, q):
    for p,u in q:
      if v == u:
        return True
    return False

  def uq(q, v, alt):
    for x, (priority, element) in enumerate(q):
      if v == element:
        _,p = q.pop(x)
        q.append((alt, p))
        return
  
  cost_dict = {}
  q = []
 
  for key,v in vdict.items():
    if v.point == s_point:
      cost_dict[v] = 0
      q.append((0, v))
    else:
      q.append((float('inf'), v))
      cost_dict[v] = float('inf')

  while q:
    q.sort(key=lambda x: x[0])
    p, u = q.pop(0)
    if p == float('inf'):
      return float('inf'), cost_dict
    for v in u.neighbors:
      if v.point == e_point and not flood:
        return cost_dict[u] + 1, cost_dict
      if fq(v,q):
        alt = cost_dict[u] + 1
        if alt < cost_dict[v]:
          cost_dict[v] = alt
          uq(q, v, alt)
  return float('inf'), cost_dict

def get_vertex(dir, point, heightmap, vdict):
  x, y = point.getxy()
  v = None
  if dir == 'D':
    if y == len(heightmap) - 1:
      return None
    np = Point(x, y + 1)
    if np in vdict.keys():
      v = vdict[np]
    else:
      v = Vertex(np, heightmap[y + 1][x])
  if dir == 'R':
    if x == len(heightmap[0]) - 1:
      return None
    np = Point(x + 1, y)
    if np in vdict.keys():
      v = vdict[np]
    else:
      v = Vertex(np, heightmap[y][x + 1])
  if v:
    vdict[np] = v
  return v

def is_possible_step(uheight, vheight):
  if (uheight == 'S' and vheight in ['a','b']) or (vheight == 'S' and uheight in ['a','b']):
    return True
  if (uheight in ['z','y'] and vheight == 'E') or (vheight in ['z','y'] and uheight == 'E'):
    return True
  if uheight == 'E':
    uheight = 'z'
  if vheight == 'E':
    vheight = 'z'
  if uheight == 'S':
    uheight = 'a'
  if vheight == 'S':
    vheight = 'a'
  vheighti = string.ascii_lowercase.find(vheight)
  uheighti = string.ascii_lowercase.find(uheight)
  return vheighti - uheighti <= 1

def connected(u, v):
  return u and v and is_possible_step(u.height, v.height)


def build_graph(heightmap, vdict):
  point = Point(0, 0)
  v0 = Vertex(point, heightmap[0][0])
  vdict[point] = v0

  # Node has a height [a-zSE] and nieghbors
  # Generate neighbors
  for y, row in enumerate(heightmap):
    for x, height in enumerate(row):
      point = Point(x, y)
      u = vdict[point]
      for dir in ('R', 'D'):
        v = get_vertex(dir, point, heightmap, vdict)
        if connected(u, v):
          u.neighbors.add(v)
        if connected(v,u):
          v.neighbors.add(u)


def main():
  file = 'C:/Users/Matthew/Desktop/input.txt'
  with open(file) as f:
    lines = f.read().splitlines()
    heightmap = build_heightmap(lines, rotate=True)
    s_point = find_points('S', heightmap).pop()
    e_point = find_points('E', heightmap).pop()
    heightmap[s_point.y][s_point.x] = 'z'
    heightmap[e_point.y][e_point.x] = 'a'
    
    vdict = {}
    build_graph(heightmap, vdict)
    score, _ = djikstra(vdict, e_point, s_point, flood=False)
    print('Part a: %i' % score)

    s_point = e_point
    e_points = find_points('z', heightmap)
    vdict = {}
    build_graph(heightmap, vdict)
    # flood just runs the pathfinding algorithm for the whole map
    # score is invalid, but then you can inspect the cost_dict for
    # things like the cheapest 'z' from a given start point
    score, cost_dict = djikstra(vdict, s_point, s_point, flood=True)
    min_cost = float('inf')
    for v, cost in cost_dict.items():
      if v.height == 'z':
        min_cost = min(min_cost, cost)
    print('Part B: %i' % min_cost)

main()