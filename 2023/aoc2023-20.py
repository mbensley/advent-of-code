# Timings: Untimed
import math
import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['']
    return test_input if test else f.read().splitlines()

OFF, ON = False,True
HIGH, LOW = 0,1
FLIPFLOP, CONJUNCTION, BROADCASTER, UNTYPED = '%', '&', 'b', 'u'
def build_modules(input):
    modules = {} # label -> (type, dests)
    state = {} # label -> state
    module_type_lookup = {}
    for line in input:
        module, dests = line.split(' -> ')   
        module_type = module[0]
        module_label = module[1:]
        if module == 'broadcaster':
            module_type = BROADCASTER
            module_label = module
        module_type_lookup[module_label] = module_type
        destinations = dests.split(', ')
        modules[module_label] = (module_type, destinations)
        state[module_label] = {FLIPFLOP: OFF, CONJUNCTION: {}, BROADCASTER: None, UNTYPED: None}[module_type]
    # second pass to input all the conjunction state
    for line in input:
        module, dests = line.split(' -> ')   
        destinations = dests.split(', ')
        module_label = module[1:]
        if module == 'broadcaster':
            module_label = module
        for dest in destinations:
            if dest not in module_type_lookup:
                modules[dest] = (UNTYPED, [])
                state[dest] = None
            elif module_type_lookup[dest] == CONJUNCTION:
                state[dest][module_label] = LOW
    return modules, state

def calc_sig(state, source, module_type, dest, signal):
    if module_type == BROADCASTER: return signal
    if module_type == FLIPFLOP:
         if signal == HIGH: return -1
         status = state[dest]
         state[dest] = not status
         if status == OFF:
             return HIGH 
         return LOW
    if module_type == CONJUNCTION:
        inputs = state[dest]
        inputs[source] = signal
        if sum(inputs.values()) == 0: return LOW
        return HIGH
    if module_type == UNTYPED:
        # Only need this for the Part B brute force method :D
        state[dest] = signal
        return -1
    raise

def simulate(modules, state, steps, spy_map):
    low_ct, high_ct = 0,0
    for step in range(steps):
        # press the button! generate a low signal
        dest_list = [('button', 'broadcaster', LOW)]
        while dest_list:
            source, dest, signal = dest_list.pop(0)
            if signal == LOW:
                low_ct += 1
            else:
                high_ct += 1
            module_type, next_dests = modules[dest]
            new_sig = calc_sig(state, source, module_type, dest, signal)
            if source in spy_map:
                if signal == HIGH:
                    spy_map[source].append(step)
            if new_sig != -1:
                dest_list.extend([(dest, next_dest, new_sig) for next_dest in next_dests])
    return low_ct * high_ct

with open(inputfile()) as f:
    input = getinput(f)
    modules, state = build_modules(input)
    print('Part A: %i' % simulate(modules, state, steps=1000, spy_map={}))

    # Part B: Brute Force >.< (~97 years?)
    if False:
        modulesb, stateb = build_modules(input)
        count = 0
        while stateb['rx'] != LOW:
            if count % 100000 == 0:
                print(count)
            simulate(modulesb, stateb, steps=1, spy_map={})
            count += 1
        print('Part B: %i' % (count+1))
    
    # Part B: Good Way (<1s)
    # based on the input, <OUTPUT> recives input from &tj (CONJUNCTION)
    # CONJUNCTIONS send low input when all of its inputs are HIGH
    # Calculate when each of it's 4 inputs (in1...in4) have all sent HIGH
    # This should have a stable period and then find the LCM of that period
    in1, in2, in3, in4 = 'xx', 'xx', 'xx', 'xx' # Change to your input values
    sample_map = {in1: [], in2: [], in3: [], in4: []}
    modulesb, stateb = build_modules(input)
    simulate(modulesb, stateb, steps=10000, spy_map=sample_map)
    print('Part B:', math.lcm(*[y-x for x,y in sample_map.values()]))