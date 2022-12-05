from pathlib import Path
import numpy as np
import re

data_path = "data/problem_04.txt"
# data_path = "data/problem_04_test.txt"



with open(data_path, "r") as f:
    data = np.array([[int(n) for n in line.replace(",", "-").split("-")] for line in f], np.int32)

a = data[:, 0]
b = data[:, 1]
c = data[:, 2]
d = data[:, 3]

# A-----B
#     C-----D

# A <= C & B >= C

#     A-----B
# C-----D

# C < A & A < D


# part 1
full_overlaps = ((a <= c) & (b >= d)) | ((b <= d) & (a >= c))
# print(full_overlaps)

print(f"Part 1 solution: {full_overlaps.sum()}")

# part 2
partial_overlaps = ~((a > d) | (b < c))
# print(partial_overlaps)

print(f"Part 2 solution: {partial_overlaps.sum()}")

