import os
import re
from collections import defaultdict
from itertools import product
from itertools import combinations
from functools import cache


class Vertex(object):

    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        # self.open = False
        self.neighbors = set()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        neighbor_names = ['%s' % n.name for n in self.neighbors]
        return '%s[%i] -> %s' % (self.name, self.flow_rate, str(neighbor_names))


def build_graph(vertex_parts):
    vertices = {}
    for vertex, neighbor_names in vertex_parts:
        vertices[vertex.name] = vertex
    for vertex, neighbor_names in vertex_parts:
        for name in neighbor_names:
            vertices[vertex.name].neighbors.add(vertices[name])
    return vertices


def parse(line):
    print(line)
    # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    valve, tunnels = line.split(';')
    name, flow_rate = re.findall(r'Valve ([A-Z]+).*=(\d+).*', valve)[0]
    neighbor_names = re.findall(r'([A-Z][A-Z])+', tunnels)
    return (Vertex(name, int(flow_rate)), neighbor_names)


class State(object):
    def __init__(self, closed_valves: set):
        # _state = valve_state  # defaultdict(lambda: False)
        self.closed_valves = closed_valves
        self.location_a = ['AA']
        self.location_b = ['AA']
        # self.prev_location_a = None
        # self.prev_location_b = None
        self.time = 0
        # self.prev_moves = []
        # self.pressure_release = 0
        # self.flow_rate = 0

    def copy(self):
        new_state = State(self.closed_valves.copy())
        new_state.location_a = self.location_a.copy()
        new_state.location_b = self.location_b.copy()
        # new_state.prev_location_a = self.prev_location_a
        # new_state.prev_location_b = self.prev_location_b
        # new_state.prev_location = self.prev_location.copy()
        # new_state.flow_rate = self.flow_rate
        new_state.time = self.time
        return new_state

    def __hash__(self):
        return hash("%s %s %s %i" % (self.closed_valves, self.location_a, self.location_b, self.time))

    def __repr__(self):
        return '%s %s [%i] %s' % (self.location_a, self.location_b, self.time, self.closed_valves)

    def __eq__(self, other):
        # and self.prev_location == other.prev_location
        return (self.location_a == other.location_a and
                self.location_b == other.location_b and
                self.time == other.time and
                self.closed_valves == other.closed_valves)


def solve_solo(state: State, time: int, location: str, flow_rate: int, prev_moves: str, edge_map: dict, flow_map: dict, seen_states: dict) -> State:
    # at any location either MOVE or OPEN, do a BFS
    # base case: no time left
    # print('Investigating %s[%i] {%s}' %
    #      (location, time_remaining, state.closed_valves))
    if time == 30:
        # print(state.closed_valves)
        seen_states[state] = flow_rate, prev_moves
        return flow_rate, prev_moves + '$'

    # base case: nothing left to open
    if not state.closed_valves:
        # print('reached end: %s' % seen_states)
        pressure, moves = solve_solo(state, time+1, location, flow_rate,
                                     prev_moves + str(time), edge_map, flow_map, seen_states)
        return pressure + flow_rate, moves
        # seen_states[state] = flow_rate + (30-time+1) * flow_rate, prev_moves
        # return flow_rate + (30-time+1) * flow_rate, prev_moves
    # cycle detected
    # if state in seen_states:
     #   print('found cycle')
        #  return 0

    max_pressure = 0
    best_prev_moves = prev_moves
    for edge in edge_map[state.location[0]]:
        # MOVE
        if state.prev_location[0] != edge:
            new_state = state.copy()
            new_state.location[0] = edge
            new_state.prev_location[0] = state.location[0]
            new_state.time = time
            if new_state in seen_states:
                # print('found solved subproblem moving')
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves + edge
            else:
                pressure, new_prev_moves = solve_solo(new_state, time+1, edge, flow_rate, prev_moves + edge, edge_map,
                                                      flow_map, seen_states)

            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = max(max_pressure, pressure)
    # OPEN
    else:
        if location in state.closed_valves:
            new_state = state.copy()
            new_state.prev_location[0] = None
            new_state.closed_valves.remove(location)
            # new_state.flow_rate += flow_map[location]
            new_state.time = time
            if new_state in seen_states:
                # print('found solved subproblem opening')
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves = new_prev_moves + ('OPEN-%s' % location)

            else:
                pressure, new_prev_moves = solve_solo(new_state, time+1, location, flow_rate+flow_map[location], prev_moves + 'OPEN-%s' % location, edge_map,
                                                      flow_map, seen_states)
            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = max(max_pressure, pressure)

    return max_pressure+flow_rate, best_prev_moves


def get_path(start, end, edge_map, v_set: set):
    # if start == 'AA':
    # print('from %s to %s' % (start, end))
    path = None
    v_set.add(start)
    for edge in edge_map[start]:
        new_set = v_set.copy()
        if edge in new_set:
            continue
        if edge == end:
            return [start, end]
        new_set.add(edge)
        next_path = get_path(edge, end, edge_map, new_set)
        if not path:
            path = next_path
        elif next_path and len(next_path) < len(path):
            path = next_path
   # if start == 'AA':
       # print('returning path %s' % path)
    if not path:
        return None
    return [start] + path


def build_path_times(edge_map):
    # build time list of times between any two points
    path_times = {}
    for start in edge_map.keys():
        path_times[start] = {}
        for end in edge_map.keys():
            if start == end:
                continue
            path_times[start][end] = len(
                get_path(start, end, edge_map, set()))
    return path_times


def generate_solutions(time: int, loc: str, flow_map: dict, closed_valves: set, path_map: dict, selected_valves: dict) -> list:
    for next_valve in closed_valves:
        path_time = path_map[loc][next_valve]
        next_time = time - path_time  # - 1
        if next_time < 1:  # takes at least 2 moves to move/open and gain flow
            continue
        new_selected_valves = selected_valves | {next_valve: next_time}
        new_closed_valves = closed_valves - {next_valve}
        yield from generate_solutions(next_time, next_valve,
                                      flow_map, new_closed_valves, path_map, new_selected_valves)

    yield selected_valves


def score_solution(flow_map: dict, selected_valves: dict) -> int:
    total = 0
    for valve, time in selected_valves.items():
        total += flow_map[valve] * time
    return total


def solve_pair_serial(flow_map, closed_valves, edge_map):
    path_map = build_path_times(edge_map)
    solutions = list(generate_solutions(time=26, loc='AA', flow_map=flow_map,
                                        closed_valves=closed_valves, path_map=path_map, selected_valves={}))
    best_score = 0
    maxscore = defaultdict(int)
    for s in solutions:
        k = frozenset(s.keys())
        new_score = score_solution(flow_map, s)
        if new_score > maxscore[k]:
            maxscore[k] = new_score
    for (v1, s1), (v2, s2) in combinations(maxscore.items(), 2):
        # for v2, s2 in maxscore.items():
        if v1.isdisjoint(v2):
            best_score = max(s1+s2, best_score)
    if False:
        for s1 in solutions:
            for s2 in solutions:
                if (len(s1) + len(s2) > 0) and set(s1.keys()).isdisjoint(set(s2.keys())):
                    score = score_solution(flow_map, s1) + \
                        score_solution(flow_map, s2)
                    best_score = max(score, best_score)
    return best_score


def solve_single(flow_map, closed_valves, edge_map):
    path_map = build_path_times(edge_map)
    solutions = generate_solutions(time=30, loc='AA', flow_map=flow_map,
                                   closed_valves=closed_valves, path_map=path_map, selected_valves={})
    best_score = 0
    for s1 in solutions:
        score = score_solution(flow_map, s1)
        best_score = max(score, best_score)
    return best_score


def solve_pair_parallel(state: State, time: int, location_a: list, location_b: list, flow_rate: int, cur_sum: int, target_a: str, target_b: str,
                        prev_moves: str, edge_map: dict, flow_map: dict, seen_states: dict) -> State:
    # fast(er) method: instead of choosing every possible move as a state, choose every possible NEXT OPEN as a possible state
    # base case: no time left
    if time == 26:
        seen_states[state] = flow_rate, prev_moves
        return flow_rate, prev_moves + '$'

    # base case: nothing left to open

    if len(state.closed_valves) == 0 and location_a == [] and location_b == []:
        a_flow = flow_map[target_a] if target_a is not None else 0
        b_flow = flow_map[target_b] if target_b is not None else 0
        if time == 11 and target_b == 'EE' and flow_rate == 78:
            print('\t[T:%i] elephant opens %s, releasing %i, sum %i' %
                  (time, target_b, flow_rate, cur_sum))  # 492
            print('New flow: %i' % (flow_rate+a_flow+b_flow))
        if time == 25 and flow_rate == 81 and cur_sum == 492+(81*14):
            print('cur_sum %i' % (cur_sum+flow_rate+a_flow+b_flow))
        pressure, moves = solve_pair_parallel(state, time+1, location_a=[], location_b=[], flow_rate=flow_rate+a_flow+b_flow, cur_sum=cur_sum+flow_rate+a_flow+b_flow, target_a=None, target_b=None,
                                              prev_moves=prev_moves + '|' + str(time), edge_map=edge_map, flow_map=flow_map,
                                              seen_states=seen_states)
        if time == 25 and flow_rate == 81 and cur_sum == 492+(81*14):
            print('pressure %i' % pressure)
        return pressure + flow_rate, moves
    max_pressure = 0
    best_prev_moves = prev_moves
    # possible states: ready to open a valve or moving to your target destination
    if target_a is None:
        cur_loc_a = 'AA'
    elif len(location_a) == 0:
        cur_loc_a = target_a
    else:
        cur_loc_a = location_a[0]
    if target_b is None:
        cur_loc_b = 'AA'
    elif len(location_b) == 0:
        cur_loc_b = target_b
    else:
        cur_loc_b = location_b[0]
    # then we're at our destination, it's time to open a valve or choose a next destination
    if len(location_a) == 0 and len(location_b) == 0 and len(state.closed_valves) > 0:
        vab_list = product(state.closed_valves, state.closed_valves)
        for va, vb in vab_list:
            if va == vb:
                continue
            new_state = state.copy()
            new_state.time = time
            new_state.closed_valves.remove(va)
            new_state.closed_valves.remove(vb)
            new_loc_a = get_path(cur_loc_a, va, set())
            new_loc_b = get_path(cur_loc_b, vb, set())
            new_state.location_a = new_loc_a[1:]
            new_state.location_b = new_loc_b[1:]
            new_path = ('|OPEN-(%s,%s)' % (target_a, target_b))
            if time == 0:
                new_path = '%s,%s' % (new_loc_a[1], new_loc_b[1])
            # ...then solve the subproblems
            if new_state in seen_states:
                print("seen previous state! closed=%i" %
                      len(new_state.closed_valves))
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves = new_prev_moves + new_path
            else:
                if (len(new_state.closed_valves) < 2):
                    print('havent seen state')
                a_flow = flow_map[target_a] if target_a != None else 0
                b_flow = flow_map[target_b] if target_b != None else 0
                if time == 7 and target_a == 'BB' and target_b == 'HH' and flow_rate == 41 and va == 'CC' and vb == 'EE':
                    print('\t[T:%i] You open %s, E opens %s, releasing %i, sum %i' %
                          (time, target_a, target_b, flow_rate, cur_sum))
                    # print('\t You path %s' % new_loc_a[1:])
                    # print('\t E path %s' % new_loc_b[1:])
                    print('\tNew flow: %i' % (flow_rate + a_flow + b_flow))
                if time == 0 and va == 'JJ' and vb == 'DD':
                    print('trying choosing %s | %s' % (va, vb))
                    print('\tYou move to %s, E move to %s' %
                          (new_loc_a[1], new_loc_b[1]))
                    print('\t%s' % new_loc_a)
                    print('\t%s' % new_loc_b)
                pressure, new_prev_moves = solve_pair_parallel(new_state, time +
                                                               1, new_loc_a[1:], new_loc_b[1:],
                                                               flow_rate + a_flow + b_flow, cur_sum=cur_sum+flow_rate+a_flow+b_flow, target_a=va, target_b=vb,
                                                               prev_moves=prev_moves + new_path,
                                                               edge_map=edge_map, flow_map=flow_map, seen_states=seen_states)
                if time == 0 and va == 'JJ' and vb == 'DD':
                    print('Final Pressure: %i [max: %i]' %
                          (pressure, max_pressure))
            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = pressure
    # if we're at loc a and still travelling for loc b
    elif len(location_a) == 0:  # and len(location_b) > 0:
        vab_list = []
        if len(state.closed_valves) == 0:
            new_state = state.copy()
            new_state.time = time
            new_state.location_b.pop(0)
            new_state.location_a = []
            a_flow = flow_map[target_a] if target_a else 0
            if target_a:
                new_path = '|OPEN-(%s),%s' % (target_a, location_b[0])
            else:
                new_path = '|X,%s' % (location_b[0])
            if time == 9 and target_a == 'CC' and target_b == 'EE' and flow_rate == 76:
                print('\t[T:%i] you open %s e moves to %s, releasing %i, sum %i' %
                      (time, target_a, location_b[0], flow_rate, cur_sum))
            if time == 10 and target_a == None and target_b == 'EE' and flow_rate == 78:
                print('\t[T:%i] you stop, e moves to %s, releasing %i, sum %i' %
                      (time,  location_b[0], flow_rate, cur_sum))
            max_pressure, new_prev_moves = solve_pair_parallel(new_state, time +
                                                               1, [], location_b[1:],
                                                               flow_rate + a_flow, cur_sum=cur_sum+flow_rate+a_flow, target_a=None, target_b=target_b,
                                                               prev_moves=prev_moves + new_path,
                                                               edge_map=edge_map, flow_map=flow_map, seen_states=seen_states)
        else:
            for va in state.closed_valves:
                # print('\tclosed valves: %s' % state.closed_valves)

                new_state = state.copy()
                new_state.time = time
                # print('\tchoosing new avalve %s' % va)
                move_b = new_state.location_b.pop(0)
                # new_state.closed_valves.remove(cur_loc_a)
                # first choose next destination_a
                new_state.closed_valves.remove(va)
                new_loc_a = get_path(cur_loc_a, va, set())
                if time == 3 and target_a == 'JJ' and target_b == 'HH' and va == 'BB' and flow_rate == 20:
                    print('\t[T:%i] Open %s, E moves to %s, releasing %i, sum %i' %
                          (time, target_a, location_b[0], flow_rate, cur_sum))
                    print('\tNext you path: %s' % new_loc_a[1:])
                # print('new a path %s' % new_loc_a)
                new_state.location_a = new_loc_a[1:]
                new_path = '|OPEN-(%s),%s' % (cur_loc_a, move_b)
                if new_state in seen_states:
                    pressure, new_prev_moves = seen_states[new_state]
                    new_prev_moves = new_prev_moves + new_path
                else:
                    flow_a = flow_map[target_a]
                    pressure, new_prev_moves = solve_pair_parallel(new_state, time +
                                                                   1, new_loc_a[1:], location_b[1:],
                                                                   flow_rate + flow_a, cur_sum=cur_sum+flow_rate+flow_a, target_a=va, target_b=target_b,
                                                                   prev_moves=prev_moves + new_path,
                                                                   edge_map=edge_map, flow_map=flow_map, seen_states=seen_states)
                if pressure > max_pressure:
                    best_prev_moves = new_prev_moves
                    seen_states[state] = pressure+flow_rate, best_prev_moves
                    max_pressure = pressure
    # if we're at loc b and still travelling for loc a
    elif len(location_b) == 0:  # and len(location_a) > 0:
        if len(state.closed_valves) == 0:
            new_state = state.copy()
            new_state.time = time
            b_flow = flow_map[target_b] if target_b else 0
            if len(location_a) == 0:
                la = 'X'
            else:
                la = location_a[0]
            if target_b:
                new_path = '|%s,OPEN-(%s)' % (la, target_b)
            elif len(location_a) > 0:
                new_path = '|%s,X' % (location_a[0])
            else:
                new_path = '|XX'
            max_pressure, new_prev_moves = solve_pair_parallel(new_state, time +
                                                               1, location_a[1:], [
                                                               ],
                                                               flow_rate + b_flow, cur_sum=cur_sum+flow_rate+b_flow, target_a=target_a, target_b=None,
                                                               prev_moves=prev_moves + new_path,
                                                               edge_map=edge_map, flow_map=flow_map, seen_states=seen_states)
        else:
            vab_list = []
            for vb in state.closed_valves:
                # print('\tclosed valves: %s' % state.closed_valves)
                new_state = state.copy()
                new_state.time = time
                # print('\tchoosing new bvalve %s' % vb)
                move_a = new_state.location_a.pop(0)
                # new_state.closed_valves.remove(cur_loc_b)
                # first choose next destination_b
                new_state.closed_valves.remove(vb)
                new_loc_b = get_path(cur_loc_b, vb, set())
                if time == 2 and target_a == 'JJ' and target_b == 'DD' and vb == 'HH':
                    print('\t[T:%i] You move to %s, E opens %s, new flow %i' %
                          (time, location_a[0], target_b, flow_rate + flow_map[target_b]))
                    print('\tNext e path: %s' % new_loc_b)
                new_state.location_b = new_loc_b[1:]
                new_path = '|%s,OPEN-(%s)' % (move_a, target_b)
                if new_state in seen_states:
                    pressure, new_prev_moves = seen_states[new_state]
                    new_prev_moves = new_prev_moves + new_path
                else:
                    flow_b = flow_map[target_b]
                    pressure, new_prev_moves = solve_pair_parallel(new_state, time +
                                                                   1, location_a[1:], new_loc_b[1:],
                                                                   flow_rate + flow_b, cur_sum=cur_sum+flow_rate+flow_b, target_a=target_a, target_b=vb,
                                                                   prev_moves=prev_moves + new_path,
                                                                   edge_map=edge_map, flow_map=flow_map, seen_states=seen_states)
                if pressure > max_pressure:
                    best_prev_moves = new_prev_moves
                    seen_states[state] = pressure+flow_rate, best_prev_moves
                    max_pressure = pressure
    # otherwise we're just moving for a and b
    else:
        if time == 1 and location_a[-1] == 'JJ' and location_b[-1] == 'DD':
            print('\t[T:%i] You move to %s, E Move %s' %
                  (time, location_a[0], location_b[0]))
        new_state = state.copy()
        new_state.time = time
        new_state.location_a.pop(0)
        new_state.location_b.pop(0)
        max_pressure, new_prev_moves = solve_pair_parallel(new_state, time+1, location_a[1:], location_b[1:],
                                                           flow_rate, cur_sum+flow_rate, target_a, target_b, prev_moves +
                                                           '|%s,%s' % (
            cur_loc_a, cur_loc_b),
            edge_map, flow_map, seen_states)
        if time == 4 and target_a == 'BB' and target_b == 'HH' and flow_rate == 41:
            print('\t[T:%i] You move to %s, E moves to %s, releasing %i, sum %i' %
                  (time, location_a[0], location_b[0], flow_rate, cur_sum))
        if time == 5 and target_a == 'BB' and target_b == 'HH' and flow_rate == 41:
            print('\t[T:%i] You move to %s, E moves to %s, releasing %i, sum %i' %
                  (time, location_a[0], location_b[0], flow_rate, cur_sum))
        if time == 6 and target_a == 'BB' and target_b == 'HH' and flow_rate == 41:
            print('\t[T:%i] You move to %s, E moves to %s, releasing %i, sum %i' %
                  (time, location_a[0], location_b[0], flow_rate, cur_sum))
        if time == 8 and target_a == 'CC' and target_b == 'EE' and flow_rate == 76:
            print('\t[T:%i] You move to %s, E moves to %s, releasing %i, sum %i' %
                  (time, location_a[0], location_b[0], flow_rate, cur_sum))
        # if pressure > max_pressure:
         #   best_prev_moves = new_prev_moves
         #
         #   max_pressure = pressure

    return max_pressure+flow_rate, best_prev_moves


def solve_pair(state: State, time: int, location_a: str, location_b: str, flow_rate: int, prev_moves: str, edge_map: dict, flow_map: dict, seen_states: dict) -> State:
    # slow method
    # at any location either MOVE or OPEN, do a BFS
    # base case: no time left
    if time == 26:
        seen_states[state] = flow_rate, prev_moves
        return flow_rate, prev_moves + '$'

    # base case: nothing left to open
    if not state.closed_valves:
        # print('reached end: %s' % seen_states)
        pressure, moves = solve_pair(state, time+1, location_a, location_b, flow_rate,
                                     prev_moves + str(time), edge_map, flow_map, seen_states)
        return pressure + flow_rate, moves

    possible_moves_a = [
        edge for edge in edge_map[location_a] if edge != state.prev_location[0]]
    if location_a in state.closed_valves:
        possible_moves_a.append('OPEN')
    possible_moves_b = [
        edge for edge in edge_map[location_b] if edge != state.prev_location[1]]
    if location_b in state.closed_valves:  # and location_b != location_a:
        possible_moves_b.append('OPEN')
    # if time < 5:
    #    print('[%s,%s] T%i: %s' % (location_a, location_b, time,
    #          list(product(possible_moves_a, possible_moves_b))))
    # try each move_a/b combination
    max_pressure = 0
    best_prev_moves = prev_moves
    for move_a, move_b in product(possible_moves_a, possible_moves_b):
        new_state = state.copy()
        new_state.time = time
        if move_a == 'OPEN' and move_b == 'OPEN':
            if location_a == location_b:
                continue
            new_state.prev_location = [None, None]
            new_state.closed_valves.remove(location_a)
            new_state.closed_valves.remove(location_b)
            if new_state in seen_states:
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves = new_prev_moves + \
                    ('|OPEN-(%s,%s)' % (location_a, location_b))
            else:
                pressure, new_prev_moves = solve_pair(
                    new_state, time+1, location_a, location_b,
                    flow_rate + flow_map[location_a] + flow_map[location_b],
                    prev_moves + '|OPEN-(%s,%s)' % (location_a, location_b),
                    edge_map, flow_map, seen_states)
            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = max(max_pressure, pressure)
        elif move_a == 'OPEN':
            if move_b == state.prev_location[1]:
                continue
            new_state.location[1] = move_b
            new_state.prev_location = [None, location_b]
            new_state.closed_valves.remove(location_a)
            new_path = '|OPEN-(%s),%s' % (location_a, move_b)
            if new_state in seen_states:
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves = new_prev_moves + new_path
            else:
                pressure, new_prev_moves = solve_pair(
                    new_state, time+1, location_a, move_b,
                    flow_rate + flow_map[location_a],
                    prev_moves + new_path,
                    edge_map, flow_map, seen_states)
            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = max(max_pressure, pressure)
        elif move_b == 'OPEN':
            if move_a == state.prev_location[0]:
                continue
            new_state.location[0] = move_a
            new_state.prev_location = [location_a, None]
            new_state.closed_valves.remove(location_b)
            new_path = '|%s,OPEN-(%s)' % (move_a, location_b)
            if new_state in seen_states:
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves = new_prev_moves + new_path
            else:
                pressure, new_prev_moves = solve_pair(
                    new_state, time+1, move_a, location_b,
                    flow_rate + flow_map[location_b],
                    prev_moves + new_path,
                    edge_map, flow_map, seen_states)
            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = max(max_pressure, pressure)
        else:
            if move_a == state.prev_location[0] and move_b == state.prev_location[1]:
                continue
            new_state.location = [move_a, move_b]
            new_state.prev_location = [location_a, location_b]
            new_path = '|%s,%s' % (move_a, move_b)
            if new_state in seen_states:
                # if location_a == 'II' and location_b == 'DD':
                #    print(new_state)
                pressure, new_prev_moves = seen_states[new_state]
                new_prev_moves = new_prev_moves + new_path
            else:
                pressure, new_prev_moves = solve_pair(
                    new_state, time+1, move_a, move_b,
                    flow_rate, prev_moves + new_path,
                    edge_map, flow_map, seen_states)
            if pressure > max_pressure:
                best_prev_moves = new_prev_moves
                seen_states[state] = pressure+flow_rate, best_prev_moves
                max_pressure = max(max_pressure, pressure)

    return max_pressure+flow_rate, best_prev_moves


with open(os.getcwd() + '/2022-16/input.txt') as f:
    vertex_parts = [parse(line) for line in f.read().splitlines()]
    # vertices = build_graph(vertex_parts)
    edge_map = {}
    closed_valves = set()
    flow_map = {}
    for vertex, neighbor_names in vertex_parts:
        edge_map[vertex.name] = neighbor_names
        if vertex.flow_rate:
            closed_valves.add(vertex.name)
            flow_map[vertex.name] = vertex.flow_rate
    # valve_state[vertex.name] = True if vertex.flow_rate == 0 else False

    state = State(closed_valves)
    # print('Part A: %i, %s' %
    #      solve_solo(state, time=1, location='AA', flow_rate=0, prev_moves='', edge_map=edge_map, flow_map=flow_map, seen_states={}))
    # print('Part B: %i, %s' %
    #      solve_pair_parallel(state=state, time=0, location_a=[], location_b=[], flow_rate=0, cur_sum=0, target_a=None, target_b=None, prev_moves='', edge_map=edge_map, flow_map=flow_map, seen_states={}))
    print('Part A: %i' % solve_single(flow_map, closed_valves, edge_map))
    print('Part B: %i' % solve_pair_serial(
        flow_map, closed_valves, edge_map))
    # 1 2 3 4BB 5 6 7 8JJ 9 10 11 12 13 14 15HH 16 17 18 19EE 20 21DD 22 23CC 24 25 26 27 28 29 30
    # BB: 26
    # JJ: 22
    # HH: 15
    # EE: 11
    # DD: 9
    # CC: 7

    # DD: 2 = 24*20
    # JJ: 3 = 23*21
    # BB: 7 = 13*19
    # HH: 7 = 22*19
    # CC: 9 = 2*17
    # EE: 11 = 3*15
