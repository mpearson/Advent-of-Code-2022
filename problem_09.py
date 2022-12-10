from pathlib import Path
import numpy as np
from math import copysign

data_path = "data/problem_09.txt"
# data_path = "data/problem_09_test_1.txt"
# data_path = "data/problem_09_test_2.txt"


DIRECTION_MAP = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}

with open(data_path, "r") as f:
    moves = []
    for line in f:
        direction, distance = line.strip().split(" ")
        dx, dy = DIRECTION_MAP[direction]

        distance = int(distance)
        moves.append((dx, dy, distance))


def print_snek(x, y, show_numbers=True):
    start_x = 11
    start_y = 15

    grid = []
    for i in range(21):
        grid.append(["."] * 26)

    for i, (x, y) in enumerate(zip(x, y)):
        if grid[start_y - y][x + start_x] == ".":
            if show_numbers:
                label = "H" if i == 0 else str(i)
            else:
                label = "#"
            grid[start_y - y][x + start_x] = label

    for row in grid:
        print("".join(row))
    print()

# part 1
head_x = head_y = tail_x = tail_y = 0

all_tail_coords = set()

for dx, dy, distance in moves:
    for _ in range(distance):
        tail_x_offset = tail_x - head_x
        tail_y_offset = tail_y - head_y

        head_x += dx
        head_y += dy



        slack_x = min(abs(tail_x_offset + dx), 1)
        slack_y = min(abs(tail_y_offset + dy), 1)

        tail_x_offset -= (slack_x * dx)
        tail_y_offset -= (slack_y * dy)

        if dx != 0 and slack_x == 0:
            tail_y_offset = 0
        if dy != 0 and slack_y == 0:
            tail_x_offset = 0

        tail_x = head_x + tail_x_offset
        tail_y = head_y + tail_y_offset

        all_tail_coords.add((tail_x, tail_y))

        # print_snek([head_x, tail_x], [head_y, tail_y])

#                             N = distance_H
#----------+------+-----------+--------------+-------------------------------+
# offset_y |  dy  | slack_y   | distance_T   | new_offset_y                  |
#----------+------+-----------+--------------+-------------------------------+
#    -1    |   1  | min(0, N) | N - slack_y  | -1                            |
#    -1    |  -1  | min(2, N) | N - slack_y  |  offset_y - min(slack_y, N)   |
#     0    |   1  | min(1, N) | N - slack_y  |                               |
#     0    |  -1  | min(1, N) | N - slack_y  |                               |
#     1    |   1  | min(2, N) | N - slack_y  |  offset_y - min(slack_y, N)   |
#     1    |  -1  | min(0, N) | N - slack_y  |  1 = offset_y - slack_y       |
#          |      |           |              |                               |

print(f"Part 1 solution: {len(all_tail_coords)}")

# import sys; sys.exit()

# part 2

N = 10
x = [0] * N
y = [0] * N
all_tail_coords = set()

def update_tail(x, y, i):
    assert i > 0
    head_x = x[i - 1]
    head_y = y[i - 1]
    offset_x = head_x - x[i]
    offset_y = head_y - y[i]

    dx = int(copysign(1, offset_x))
    dy = int(copysign(1, offset_y))
    distance_x = abs(offset_x)
    distance_y = abs(offset_y)

    if distance_y > 1:
        y[i] += dy * (distance_y - 1)

    if distance_x > 1:
        x[i] += dx * (distance_x - 1)

    if distance_y > 1 and distance_x <= 1:
        x[i] = head_x
    if distance_x > 1 and distance_y <= 1:
        y[i] = head_y

for move_index, (head_dx, head_dy, distance) in enumerate(moves):
    # print(f"move {move_index}: {head_dx}, {head_dy}, {distance}")
    for _ in range(distance):
        x[0] += head_dx
        y[0] += head_dy

        for i in range(1, N):
            update_tail(x, y, i)

        # print_snek(x, y)
        all_tail_coords.add((x[-1], y[-1]))

tail_trail = np.array(list(all_tail_coords))
print(tail_trail.shape)
# print_snek(tail_trail[:,0], tail_trail[:,1], show_numbers=False)


print(f"Part 2 solution: {len(all_tail_coords)}")
