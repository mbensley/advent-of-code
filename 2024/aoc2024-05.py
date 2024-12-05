import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['']
    return test_input if test else f.read()

def is_valid(rules, update):
    for r0, r1 in rules:
        if r0 in update and r1 in update:
            if update.index(r0) > update.index(r1):
                return False, (r0,r1)
    return True, None

def sum_valid_mids(rules, updates):
    total = 0
    for update in updates:
        update = update.split(',')
        if is_valid(rules, update)[0]:
            total += int(update[len(update)//2])
    return total


def sum_invalid_mids(rules, updates):
    total = 0
    for update in updates:
        update = update.split(',')
        valid, rule = is_valid(rules, update)
        if not valid:
            while not valid:
                update[update.index(rule[0])] = rule[1]
                update[update.index(rule[1])] = rule[0]
                valid, rule = is_valid(rules, update)
            total += int(update[len(update)//2])
    return total

def build_rules(rules):
    rule_list = []
    for rule in rules:
        rule_list.append(rule.split('|'))
    return rule_list

with open(inputfile()) as f:
    input = getinput(f)
    rules, updates = input.split('\n\n')
    print('Part A: %i' % sum_valid_mids(build_rules(rules.splitlines()), updates.splitlines()))
    print('Part B: %i' % sum_invalid_mids(build_rules(rules.splitlines()), updates.splitlines()))
