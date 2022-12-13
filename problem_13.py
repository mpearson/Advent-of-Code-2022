import json
from functools import cmp_to_key
import numpy as np

data_path = "data/problem_13.txt"
# data_path = "data/problem_13_test.txt"

def load():
    with open(data_path, "r") as f:
        lines = f.readlines()

    pairs = []
    for index in range(0, len(lines), 3):
        pairs.append((
            json.loads(lines[index]),
            json.loads(lines[index + 1]),
        ))

    return pairs


def compare(left, right, depth=0):
    if isinstance(left, int):
        if isinstance(right, int):
            return left - right
        left = [left]
    elif isinstance(right, int):
        right = [right]

    for i in range(min(len(left), len(right))):
        item_result = compare(left[i], right[i], depth + 1)
        if item_result != 0:
            return item_result

    return len(left) - len(right)

# part 1
pairs = load()
results = [compare(*pair) < 1 for pair in pairs]
# for index, result in enumerate(results):
#     print(index + 1, result)


print(f"Part 1 solution: {np.sum(np.nonzero(results)[0] + 1)}")

# part 2
packets = []
for pair in pairs:
    packets.extend(pair)

divider_packets = ([[2]], [[6]])
packets.extend(divider_packets)
packets.sort(key=cmp_to_key(compare))
# for packet in packets:
#     print(packet)

print(f"Part 2 solution: {(packets.index(divider_packets[0]) + 1) * (packets.index(divider_packets[1]) + 1)}")

