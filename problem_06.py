import time
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

data_path = "data/problem_06.txt"
# data_path = "data/problem_06_test.txt"

datasets = []
CHAR_OFFSET = ord("a")
with open(data_path, "r") as f:
    for line in f:
        datasets.append(np.array([ord(c) - CHAR_OFFSET for c in line[:-1]], dtype=np.uint32))

# part 1
def find_the_thingy_v1(buffer):
    window = sliding_window_view(buffer, 4)  # magical sliding window that acts like a regular array
    window_uniqueness = (
        (window[:, 0] != window[:, 1]) &
        (window[:, 0] != window[:, 2]) &
        (window[:, 0] != window[:, 3]) &
        (window[:, 1] != window[:, 2]) &
        (window[:, 1] != window[:, 3]) &
        (window[:, 2] != window[:, 3])
    )
    # find the first window position where all values are unique
    return np.argmax(window_uniqueness) + 4

# for buffer in datasets:
#     print(find_the_thingy_v1(buffer))

print(f"Part 1 solution: {find_the_thingy_v1(datasets[0])}")


# part 2
def find_the_thingy_v2(buffer):
    # embiggened version of v1
    window = sliding_window_view(buffer, 14)
    window_uniqueness = (
        (window[:, 0] != window[:, 1]) &
        (window[:, 0] != window[:, 2]) &
        (window[:, 0] != window[:, 3]) &
        (window[:, 0] != window[:, 4]) &
        (window[:, 0] != window[:, 5]) &
        (window[:, 0] != window[:, 6]) &
        (window[:, 0] != window[:, 7]) &
        (window[:, 0] != window[:, 8]) &
        (window[:, 0] != window[:, 9]) &
        (window[:, 0] != window[:, 10]) &
        (window[:, 0] != window[:, 11]) &
        (window[:, 0] != window[:, 12]) &
        (window[:, 0] != window[:, 13]) &

        (window[:, 1] != window[:, 2]) &
        (window[:, 1] != window[:, 3]) &
        (window[:, 1] != window[:, 4]) &
        (window[:, 1] != window[:, 5]) &
        (window[:, 1] != window[:, 6]) &
        (window[:, 1] != window[:, 7]) &
        (window[:, 1] != window[:, 8]) &
        (window[:, 1] != window[:, 9]) &
        (window[:, 1] != window[:, 10]) &
        (window[:, 1] != window[:, 11]) &
        (window[:, 1] != window[:, 12]) &
        (window[:, 1] != window[:, 13]) &

        (window[:, 2] != window[:, 3]) &
        (window[:, 2] != window[:, 4]) &
        (window[:, 2] != window[:, 5]) &
        (window[:, 2] != window[:, 6]) &
        (window[:, 2] != window[:, 7]) &
        (window[:, 2] != window[:, 8]) &
        (window[:, 2] != window[:, 9]) &
        (window[:, 2] != window[:, 10]) &
        (window[:, 2] != window[:, 11]) &
        (window[:, 2] != window[:, 12]) &
        (window[:, 2] != window[:, 13]) &

        (window[:, 3] != window[:, 4]) &
        (window[:, 3] != window[:, 5]) &
        (window[:, 3] != window[:, 6]) &
        (window[:, 3] != window[:, 7]) &
        (window[:, 3] != window[:, 8]) &
        (window[:, 3] != window[:, 9]) &
        (window[:, 3] != window[:, 10]) &
        (window[:, 3] != window[:, 11]) &
        (window[:, 3] != window[:, 12]) &
        (window[:, 3] != window[:, 13]) &

        (window[:, 4] != window[:, 5]) &
        (window[:, 4] != window[:, 6]) &
        (window[:, 4] != window[:, 7]) &
        (window[:, 4] != window[:, 8]) &
        (window[:, 4] != window[:, 9]) &
        (window[:, 4] != window[:, 10]) &
        (window[:, 4] != window[:, 11]) &
        (window[:, 4] != window[:, 12]) &
        (window[:, 4] != window[:, 13]) &

        (window[:, 5] != window[:, 6]) &
        (window[:, 5] != window[:, 7]) &
        (window[:, 5] != window[:, 8]) &
        (window[:, 5] != window[:, 9]) &
        (window[:, 5] != window[:, 10]) &
        (window[:, 5] != window[:, 11]) &
        (window[:, 5] != window[:, 12]) &
        (window[:, 5] != window[:, 13]) &

        (window[:, 6] != window[:, 7]) &
        (window[:, 6] != window[:, 8]) &
        (window[:, 6] != window[:, 9]) &
        (window[:, 6] != window[:, 10]) &
        (window[:, 6] != window[:, 11]) &
        (window[:, 6] != window[:, 12]) &
        (window[:, 6] != window[:, 13]) &

        (window[:, 7] != window[:, 8]) &
        (window[:, 7] != window[:, 9]) &
        (window[:, 7] != window[:, 10]) &
        (window[:, 7] != window[:, 11]) &
        (window[:, 7] != window[:, 12]) &
        (window[:, 7] != window[:, 13]) &

        (window[:, 8] != window[:, 9]) &
        (window[:, 8] != window[:, 10]) &
        (window[:, 8] != window[:, 11]) &
        (window[:, 8] != window[:, 12]) &
        (window[:, 8] != window[:, 13]) &

        (window[:, 9] != window[:, 10]) &
        (window[:, 9] != window[:, 11]) &
        (window[:, 9] != window[:, 12]) &
        (window[:, 9] != window[:, 13]) &

        (window[:, 10] != window[:, 11]) &
        (window[:, 10] != window[:, 12]) &
        (window[:, 10] != window[:, 13]) &

        (window[:, 11] != window[:, 12]) &
        (window[:, 11] != window[:, 13]) &

        (window[:, 12] != window[:, 13])
    )
    return np.argmax(window_uniqueness) + 14


def find_the_thingy_v3(buffer, window_size):
    # Since we only have 26 values but at least 32 bits in an int, we can map each value onto a
    # unique bit position. Then we can bitwise OR all the bits within a given sliding window.
    # This orthogonally encodes the presence of each unique symbol in the resulting int.
    sliding_window = sliding_window_view(1 << buffer, window_size)
    window_uniqueness = np.bitwise_or.reduce(sliding_window, axis=1)

    # Compute the hamming weight (number of 1 bits)
    count = np.zeros_like(window_uniqueness)
    for i in range(26):  # only need to check the first 26 bit positions
        mask = window_uniqueness != 0
        count[mask] += 1
        window_uniqueness[mask] &= window_uniqueness[mask] - 1

    # Find the first offset with the desired number of 1 bits
    return np.argmax(count == window_size) + window_size


print(f"Part 2 solution: {find_the_thingy_v3(datasets[0], 14)}")


# comparing v2 and v3 performance, sadly v3 is not as fast as v2 despite being cooler
N = 100
t0 = time.perf_counter()
for i in range(N):
    x = find_the_thingy_v2(datasets[0])
print(f"v2: {time.perf_counter() - t0}")


t0 = time.perf_counter()
for i in range(N):
    x = find_the_thingy_v3(datasets[0], 14)
print(f"v3: {time.perf_counter() - t0}")
