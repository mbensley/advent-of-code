from itertools import product
import sys

def check_exterior(point, pset, eset,nset, iset, maxc):
  # needs to differentiate between running into a shape or starting on a shape
  #print(point)
  if point in pset or point in iset:
    
    return False
  if point in eset:
    return True
  # otherwise run recursively, check if any adjacent point is exterior
  
  dps = ((1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1))
  x,y,z = point
  # check each direction
  any_ext = False
  for dx,dy,dz in dps:
    dpoint = (x+dx,y+dy,z+dz)
    if dpoint in nset:
      continue
    if dpoint in iset:
      return False
    nset.add(point)
    if maxc < x+dx or maxc < y+dy or maxc < z+dz or x+dx <= 0 or y+dy<=0 or z+dz<=0:
      eset.update(nset)
      eset.add(dpoint)
      
      any_ext = True
    elif check_exterior(dpoint,pset,eset,nset,iset, maxc):
      eset.add(dpoint)
      eset.update(nset)
      any_ext= True
  #if not any_ext:
   # print('found interior: %s' % str(point))
  return any_ext

sys.setrecursionlimit(100000) 
with open('i.txt') as f:
  maxc = 0
  pset = set()
  transitions = 0
  dps = ((1,0,0),(0,1,0),(0,0,1))
  for line in f.read().splitlines():
    x,y,z = line.split(',')
    x,y,z = int(x), int(y), int(z)
    maxc = max(maxc,x,y,z)
    pset.add((x,y,z))
    # check each direction
    for dp in dps:
      if (x+dp[0],y+dp[1],z+dp[2]) not in pset:
        transitions += 1
      if (x-dp[0],y-dp[1],z-dp[2]) in pset:
        transitions -= 1
  print(len(pset))
  print(pset)
  print('Part A: %i' % (transitions*2))
  interior_set = set()
  epset = pset.copy()
  maxc += 1
  print(maxc)
  #maxc = 16
  eset = set()

  #print(check_exterior((2,2,5),epset,eset,set(), maxc))


  for point in product(range(maxc),range(maxc),range(maxc)):
    #print(point)
    if not check_exterior(point, epset, eset, set(), interior_set, maxc) and point not in epset:
      interior_set.add(point)
     # epset.add(point)
  print(interior_set)
  transitionsB = 0
  dps = ((1,0,0),(0,1,0),(0,0,1))
  new_set = set() 
 # print(new_set)
  #print(len(epset))
 # print(len(interior_set))
  #print(len(new_set))
  for x,y,z in epset.union(interior_set):
    # check each direction
    new_set.add((x,y,z))
    for (dx,dy,dz) in dps:
      if (x+dx,y+dy,z+dz) not in new_set:
        transitionsB += 1
      if (x-dx,y-dy,z-dz) in new_set:
        transitionsB -= 1
  print(maxc)
  print('Part B: %i' % (transitionsB*2))
    
    
# calculate reachability of every point in the bounding box?
# any way to fill in the shape?
# find all connected points that cant reach the bounding box and add those points to the set