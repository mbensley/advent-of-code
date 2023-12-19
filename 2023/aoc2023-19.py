# Timings: Part A: 20:00 / Part B: Untimed
import os
from copy import deepcopy


def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = 'in{a<3:m,R}\nm{m<3:x,R}\nx{x<3:s,R}\ns{s<3:A,R}\n\n{x=1,m=1,s=1,a=1}'
    return test_input if test else f.read()

def build_workflows(input):
    w = {}
    for line in input.splitlines():
        label, r = line.split('{')
        r = r[:-1]
        rules = []
        for rule in r.split(','):
            rules.append(rule)
        w[label] = rules
    return w

def build_parts(input):
    parts = []
    for line in input.splitlines():
        l = line[1:-1]
        part = {}
        for tk in l.split(','):
            label, val = tk.split('=')
            part[label] = int(val)
        parts.append(part)
    return parts

def calc(part, workflows, start):
    workflow = workflows[start]
    while True:
        for test in workflow:
            if test == 'A': return True
            if test == 'R': return False
            if ':' not in test:
                return calc(part, workflows, test)
            rule, next_label = test.split(':')
            if '>' in rule:
                sym = '>'
                prop, target = rule.split('>')
                if part[prop] > int(target):
                    if next_label == 'A': return True
                    if next_label == 'R': return False
                    return calc(part, workflows, next_label)
            if '<' in rule:
                sym = '<'
                prop, target = rule.split('<')
                if part[prop] < int(target):
                    if next_label == 'A': return True
                    if next_label == 'R': return False
                    return calc(part, workflows, next_label)

def calc_total(workflows, start, rdict):
    def c(d):
        product = 1
        for v in d.values():
            product *= ((v[1]+1) - (v[0]))
        return product
    
    def splitrange(splitval, r, splitsym):
        rmin, rmax = r
        midpoint = splitval - 1 if splitsym == '<' else splitval
        lmin,lmax = rmin,midpoint
        rmin,rmax = midpoint+1,rmax
        return [lmin,lmax],[rmin,rmax]
    
    total = 0
    if start == 'A': return c(rdict)
    if start == 'R': return 0
    for test in workflows[start]:
        # for each test, split the range into valid/invalid
        if test == 'A': return total + c(rdict) # everything is valid and we're done
        if test == 'R': return total # nothing is valid and we're done
        validdict = deepcopy(rdict)
        # keep going, send all ranges to the next workflow
        if ':' not in test: return total + calc_total(workflows, test, validdict)
        rule, pass_label = test.split(':')
        if '>' in rule:
            key, val = rule.split('>')
            val = int(val)
            # split the range into valid and invalid
            l,r = splitrange(val, rdict[key], '>')
            validdict[key] = r
            # The invalid range just resets the range in rdict and continues  
            rdict[key] = l
            total += calc_total(workflows, pass_label, validdict)
        if '<' in rule:
            key, val = rule.split('<')
            val = int(val)
            # split the range into valid and invalid
            l,r = splitrange(val, rdict[key], '<')
            validdict[key] = l
            # The invalid range just resets the range in rdict and continues
            rdict[key] = r
            total += calc_total(workflows, pass_label, validdict)
    raise # everything should resolve to an A or R eventually

with open(inputfile()) as f:
    input = getinput(f)
    w, p = input.split('\n\n')
    parts = build_parts(p)
    workflows = build_workflows(w)
    tot_ratings = 0
    start_workflow = 'in'

    # Part A
    for part in parts:
        if calc(part, workflows, start_workflow):
            tot_ratings += sum(part.values())

    print('Part A: %i' % tot_ratings)
    print('Part B: %i' % calc_total(workflows, start_workflow,
                                           {'x': [1, 4000],
                                            'm': [1, 4000],
                                            'a': [1, 4000],
                                            's':[1, 4000]}))
