import re


def parse(line):
    print(line)
    # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    valve, tunnels = line.split(';')
    name, flow_rate = re.findall(r'Valve ([A-Z]+).*=(\d+).*', valve)[0]
    neighbor_names = re.findall(r'([A-Z][A-Z])+', tunnels)
    return ((name, int(flow_rate)), neighbor_names)


def parse_blueprint(line: str):
    # Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    id, oreOreR, clayOreR, obsOreR, obsClayR, geoOreR, geoObsR = re.findall(
        r'(\d+)', line)
    return (int(x) for x in (id, oreOreR, clayOreR, obsOreR, obsClayR, geoOreR, geoObsR))
