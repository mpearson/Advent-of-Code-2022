import re
from pathlib import Path
from dataclasses import dataclass
import numpy as np

data_path = "data/problem_16.txt"
data_path = "data/problem_16_test.txt"

FILE_REGEX = re.compile(
    r"Valve (?P<name>[A-Z]{2}) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<neighbors>[\w, ]+)"
)


@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbors: list

    @classmethod
    def from_text(cls, line):
        m = FILE_REGEX.match(line)
        return cls(
            m.group("name"),
            int(m.group("flow_rate")),
            m.group("neighbors").split(", ")
        )


def load():
    with open(data_path, "r") as f:
        valve_dict = {}
        for line in f:
            valve = Valve.from_text(line[:-1])
            valve_dict[valve.name] = valve

    for valve in valve_dict.values():
        valve.neighbors = [valve_dict[neighbor] for neighbor in valve.neighbors]

    return valve_dict


# print(data)


valve_dict = load()
# print(valve_dict.keys())

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
# Valve BB has flow rate=13; tunnels lead to valves CC, AA
# Valve CC has flow rate=2; tunnels lead to valves DD, BB




# part 1
print(f"Part 1 solution: {None}")

# part 2
print(f"Part 2 solution: {None}")

