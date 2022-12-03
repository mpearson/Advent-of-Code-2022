from pathlib import Path
import numpy as np

data_path = "data/problem_03.txt"
# data_path = "data/problem_03_test.txt"

# part 1

lower_offset = ord("a") - 1
upper_offset = ord("A") - 27
def get_priority(char):
    char = ord(char)
    if char < lower_offset:
        return char - upper_offset
    else:
        return char - lower_offset

total = 0
with open(data_path, "r") as f:
    for line in f:
        line = line.strip()
        half_length = len(line) // 2
        letter = tuple(set(line[:half_length]).intersection(line[half_length:]))[0]
        priority = get_priority(letter)
        total += priority
        # print(letter, priority)

print(f"Part 1 solution: {total}")

# part 2

total = 0
with open(data_path, "r") as f:
    elf_index = 0
    group_items = None
    for line in f:
        if elf_index == 0:
            group_items = set(line.strip())
        else:
            group_items.intersection_update(line.strip())
        elf_index += 1

        if elf_index == 3:
            elf_index = 0
            assert len(group_items) == 1
            letter = tuple(group_items)[0]
            priority = get_priority(letter)
            total += priority
            # print(letter, priority)

print(f"Part 2 solution: {total}")

