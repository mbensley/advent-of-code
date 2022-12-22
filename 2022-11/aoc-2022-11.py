import math

def computeGCD(x, y):
 
    if x > y:
        small = y
    else:
        small = x
    print(small)
    for i in range(1, small + 1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i
             
    return gcd

class Monkey(object):
  def __init__(self, item_list, op_fn, test_div, true_target, false_target):
    self.item_list = item_list
    self.op_fn = op_fn
    self.test_div = test_div
    self.true_target = true_target
    self.false_target = false_target
    self.inspections = 0

  def take_turn(self, monkey_list):
    for _ in range(len(self.item_list)):
      # inspect item
      self.inspections += 1
      item = self.item_list.pop(0)
      item = item % 223092870
      #print('Testing item %i' % item)
      item = self.op_fn(item)
     # print('modifying item to %i' % item)
      #item = math.floor(item / 3)
      #print('relief item to %i' % item)
      # test
      if item % self.test_div == 0:
        #print('divisible!throwing %i to %i' % (self.test_div, self.true_target))
        monkey_list[self.true_target].item_list.append(item)
        
      else:
        #x = math.floor(item // self.test_div)
        #rem = math.floor(item % self.test_div)
        #gcf = computeGCD(x, rem)
        #print('%i: %i * %i + %i' % (item, (x/gcf), self.test_div, (rem/gcf)))
        monkey_list[self.false_target].item_list.append(item)
        #monkey_list[self.false_target].item_list.append(((self.test_div * (x//gcf)) + (rem//gcf)))
        #monkey_list[self.false_target].item_list.append((item // self.test_div)*self.test_div  + (item % self.test_div))
  # 2, 3, 5, 7, 11, 13, 17, 19
  # td = 17
  # item = 34 => 17 == 2 * 17
        # 350 % 17 == 10 => 20 * 17 + 10
        #17 and 27 % 

def main():
  rounds = 10000
  monkey_list = [
    Monkey([65, 58, 93, 57, 66], lambda x: x*7, 19, 6, 4),
    Monkey([76, 97, 58, 72, 57, 92, 82], lambda x: x+4, 3, 7, 5),
    Monkey([90, 89, 96], lambda x: x*5, 13, 5, 1),
    Monkey([72, 63, 72, 99], lambda x: x*x, 17, 0, 4),
    Monkey([65], lambda x: x+1, 2, 6, 2),
    Monkey([97, 71], lambda x: x+8, 11, 7, 3),
    Monkey([83, 68, 88, 55, 87, 67], lambda x: x+2, 5, 2, 1),
    Monkey([64, 81, 50, 96, 82, 53, 62, 92], lambda x: x+5, 7, 3, 0)]
  #monkey_list = [
  #  Monkey([79, 98], lambda x: x*19, 23, 2, 3),
  #  Monkey([54, 65, 75, 74], lambda x: x+6, 19, 2, 0),
  #  Monkey([79, 60, 97], lambda x: x*x, 13, 1, 3),
  #  Monkey([74], lambda x: x+3, 17, 0, 1)]
  for round in range(rounds):
    for monkey in monkey_list:
      monkey.take_turn(monkey_list)

  inspect_list = []
  for monkey in monkey_list:
    inspect_list.append(monkey.inspections)
    #sum += monkey.inspections
  inspect_list.sort()
  print(inspect_list)
  print(inspect_list[-1] * inspect_list[-2])
#print(sum) 
main()