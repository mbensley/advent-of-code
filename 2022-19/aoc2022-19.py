import os
import re
from math import ceil

ORE_IDX = 0
CLAY_IDX = 1
OBS_IDX = 2
GEODE_IDX = 3


def get_goals():
    return [GEODE_IDX, OBS_IDX, CLAY_IDX, ORE_IDX]


def tsum(t0, t1, subtract=False):
    return [x+y if not subtract else x-y for x, y in zip(t0[:], t1[:])]


def parse_blueprint(line: str):
    # Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    id, oreOreR, clayOreR, obsOreR, obsClayR, geoOreR, geoObsR = re.findall(
        r'(\d+)', line)
    return (int(x) for x in (id, oreOreR, clayOreR, obsOreR, obsClayR, geoOreR, geoObsR))


def calc_max_geodes(time: int, stock: tuple, robots: tuple, goal: int, rcost: dict, maxseen: int):
    # stock = (ore, clay, obsidian, geode)
    # robots = (oreR, clayR, obsR, geodeR) # target index is 0-3 index into robots
    # For each call, choose each next robot and take the max geodes as the answer
    # Step: choose a next target robot to build that's possible given current robots
    # Prune here
    # check the theoretical max left
    global max_q
    tmax = stock[GEODE_IDX] + \
        (time)*(robots[GEODE_IDX]+1) + (time*(time-1) // 2)
    if tmax <= max_q:
        return
    # No clay so can never build the OBS goal
    if goal == OBS_IDX and robots[CLAY_IDX] == 0:
        return
    # No OBS so can never build the GEODE goal
    if goal == GEODE_IDX and robots[OBS_IDX] == 0:
        return
    # never need to build more robots of one kind than the max costs
    # max_ore, max_clay, max_obs = 0
    max_ore = max(c[0] for c in rcost.values())
    max_clay = max(c[1] for c in rcost.values())
    max_obs = max(c[2] for c in rcost.values())
    if (robots[ORE_IDX] > max_ore or
        robots[CLAY_IDX] > max_clay or
            robots[OBS_IDX] > max_obs):
        return

    while time:
        t = time - 1
        cost = rcost[goal]
        needed_stock = [abs(x) if x < 0 else 0 for x in tsum(
            stock, cost, subtract=True)]
        if goal == ORE_IDX:
            if not any(needed_stock):
                new_robots = tsum(robots, (1, 0, 0, 0))
                for g in get_goals():
                    new_stock = tsum(tsum(stock, robots), cost, subtract=True)
                    calc_max_geodes(
                        t, new_stock, new_robots, g, rcost, new_stock[GEODE_IDX])
                return

        elif goal == CLAY_IDX:
            if not any(needed_stock):
                new_robots = tsum(robots, (0, 1, 0, 0))
                for g in get_goals():
                    new_stock = tsum(tsum(stock, robots), cost, subtract=True)
                    calc_max_geodes(
                        t, new_stock, new_robots, g, rcost, new_stock[GEODE_IDX])
                return

        elif goal == OBS_IDX:
            if not any(needed_stock):
                new_robots = tsum(robots, (0, 0, 1, 0))
                for g in get_goals():
                    new_stock = tsum(tsum(stock, robots), cost, subtract=True)
                    calc_max_geodes(
                        t, new_stock, new_robots, g, rcost, new_stock[GEODE_IDX])
                return

        elif goal == GEODE_IDX:
            if not any(needed_stock):
                new_robots = tsum(robots, (0, 0, 0, 1))
                for g in get_goals():
                    new_stock = tsum(tsum(stock, robots), cost, subtract=True)
                    calc_max_geodes(
                        t, new_stock, new_robots, g, rcost, new_stock[GEODE_IDX])
                return

        stock = tsum(stock, robots)
        # max_q = max(max_q, stock[GEODE_IDX])  # max_geodes + stock[GEODE_IDX]
        time -= 1
        # return max(max_geodes, calc_max_geodes(
        #    t, new_stock, robots, goal, rcost, new_stock[GEODE_IDX]))
    # return max_geodes
    # print('found time: %i' % time)

    max_q = max(max_q, stock[GEODE_IDX])
    return

    if False:
        new_time = time
        new_robots = robots[:]
        # Step 0: calc time to build target robot
        cost = rcost[choice]
        needed_stock = [abs(x) if x < 0 else 0 for x in tsum(
            new_stock, cost, subtract=True)]
        while any(needed_stock) and new_time <= maxtime:

            new_stock = tsum(new_stock, new_robots, subtract=False)
            new_time += 1
            needed_stock = [abs(x) if x < 0 else 0 for x in tsum(
                            new_stock, cost, subtract=True)]

        if new_time >= maxtime:
            max_geodes = max(
                max_geodes, new_stock[GEODE_IDX])  # +new_robots[GEODE_IDX])
            # continue
        time_left = maxtime-new_time

        # step 1: build robot (remove stock)
        new_stock = tsum(new_stock, cost, subtract=True)
        # Step 2: collect minerals for this turn
        new_stock = tsum(new_stock, new_robots)
        # Step 3: robot it ready, update robots
        new_robots[choice] += 1

        # Step 4: recurse
        # print("Recursing with new time: %i" % (time_left - time_cost))
        next_possible_choices = []
        # sum(x for x in range(time_left)):
        if maxseen <= time_left*stock[GEODE_IDX]+(time_left*(time_left-1)):
            if maxseen > 0:
                print('T%i stock %s, maxseen: %i, theoretical max: %i' % (new_time, new_stock,
                                                                          maxseen,  time_left*new_stock[GEODE_IDX]+(time_left*(time_left-1))))
            if tsum(new_stock, rcost[ORE_IDX], subtract=True)[0] < 0 and time_left > 2:
                next_possible_choices.append(ORE_IDX)
            if tsum(new_stock, rcost[CLAY_IDX], subtract=True)[0] < 0 and time_left > 2:
                next_possible_choices.insert(0, CLAY_IDX)
            # possible_choices.extend([CLAY_IDX, ORE_IDX])
            # only need to potentially add obs/geode. ore/clay/skip are always possible
            # obs_cost = tsum(stock, rcost[OBS_IDX], subtract=True)
            # OBS is made of Ore+Clay
            # and obs_cost[0] < 0 and obs_cost[1] < 0 and time_left > 3:
            if robots[CLAY_IDX] > 0:
                next_possible_choices.insert(0, OBS_IDX)
            # geode_cost = tsum(stock, rcost[GEODE_IDX], subtract=True)
            # GEODE is made of Ore+Obsidian
            # and geode_cost[0] < 0 and geode_cost[2] < 0 and time_left > 1:
            if robots[OBS_IDX] > 0:
                next_possible_choices.insert(0, GEODE_IDX)

            # print('possible choices for next choice: %s' % next_possible_choices)
            max_geodes = max(max_geodes, calc_max_geodes(
                new_time+1, maxtime, new_stock[:],
                new_robots[:],
                possible_choices=next_possible_choices[:],
                rcost=rcost, maxseen=max(maxseen, stock[GEODE_IDX])))
        return max_geodes


with open(os.getcwd() + '/2022-19/input-t.txt') as f:
    qsum = 0
    for line in f.read().splitlines():
        id, oreOreR, clayOreR, obsOreR, obsClayR, geoOreR, geoObsR = parse_blueprint(
            line)
        cost_dict = {
            ORE_IDX: (oreOreR, 0, 0, 0),
            CLAY_IDX: (clayOreR, 0, 0, 0),
            OBS_IDX: (obsOreR, obsClayR, 0, 0),
            GEODE_IDX: (geoOreR, 0, geoObsR, 0)}
        q = 0
        max_q = 0
        for g in get_goals():
            calc_max_geodes(time=24,  # 32 for part B
                            stock=(0, 0, 0, 0),
                            robots=(1, 0, 0, 0),
                            goal=g,
                            rcost=cost_dict,
                            maxseen=0)
            # print('finished %i: %i' % (g, max_q))
        print('%i: %i' % (id, max_q))
        qsum += max_q*id
    print('Part A: %i' % qsum)
