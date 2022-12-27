import re
from pathlib import Path
import numpy as np

data_path = "data/problem_22.txt"
# data_path = "data/problem_22_test.txt"


# data = np.genfromtxt(data_path, dtype=np.int32)

with open(data_path, "r") as f:
    data = f.read().splitlines()

instructions = data[-1]
map_lines = data[:-2]

headings = np.array([
    (0, 1),     # east
    (1, 0),     # south
    (0, -1),    # west
    (-1, 0),    # north
])


map_width = max((len(line) for line in map_lines))
print(map_width)

print(map_lines[-5:])

print(re.split("([LR])", instructions))
instructions
# print(data)

# part 1
print(f"Part 1 solution: {None}")

# part 2
print(f"Part 2 solution: {None}")

