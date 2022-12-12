from pathlib import Path
import numpy as np

data_path = "data/problem_01.txt"
# data_path = "data/problem_01_test.txt"


# part 1
max_payload = 0
with open(data_path, "r") as f:
    payload = 0
    for line in f:
        line = line.strip()
        if line:
            payload += int(line)
        else:
            max_payload = max(max_payload, payload)
            payload = 0

    max_payload = max(max_payload, payload)

print(f"Part 1 solution: {max_payload}")

# part 2
top_list = [0] * 3
def update_top_list(x):
    for index in range(len(top_list)):
        if x > top_list[index]:
            x, top_list[index] = top_list[index], x

with open(data_path, "r") as f:
    payload = 0
    for line in f:
        line = line.strip()
        if line:
            payload += int(line)
        else:
            update_top_list(payload)
            payload = 0

    update_top_list(payload)

print(f"Part 2 solution: {sum(top_list)}")

