from pathlib import Path
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


def load_moves():
    with open(data_path, "r") as f:
        moves = []
        for line in f:
            direction, distance = line.strip().split(" ")
            dx, dy = DIRECTION_MAP[direction]

            distance = int(distance)
            moves.append((dx, dy, distance))

    return moves


def print_snek(positions, show_numbers=True):
    import numpy as np
    positions = np.asarray(positions)
    # min_coords = positions.min(axis=0)
    # max_coords = positions.max(axis=0)
    # shape = ((max_coords - min_coords) + 1)[::-1]
    # positions[:, 0] = positions[:, 0] - min_coords[0]
    # positions[:, 1] = min_coords[1] - positions[:, 1] - 1
    shape = (21, 26)
    start_x = 11
    start_y = 15
    positions[:, 0] = positions[:, 0] + start_x
    positions[:, 1] = start_y - positions[:, 1]
    grid = []
    for i in range(shape[0]):
        grid.append(["."] * shape[1])

    for i, (x, y) in enumerate(positions):
        if grid[y][x] == ".":
            if show_numbers:
                label = "H" if i == 0 else str(i)
            else:
                label = "#"
            grid[y][x] = label

    for row in grid:
        print("".join(row))
    print()


def update_snek(segment_pos, head_pos):
    offset_x = head_pos[0] - segment_pos[0]
    offset_y = head_pos[1] - segment_pos[1]
    distance_x = abs(offset_x)
    distance_y = abs(offset_y)
    if distance_y > 1:
        segment_pos[1] += int(copysign(distance_y - 1, offset_y))
        if distance_x <= 1:
            segment_pos[0] = head_pos[0]
    if distance_x > 1:
        segment_pos[0] += int(copysign(distance_x - 1, offset_x))
        if distance_y <= 1:
            segment_pos[1] = head_pos[1]


def snek(snek_size, moves):
    all_tail_coords = set()
    positions = [[0, 0] for _ in range(snek_size)]
    for head_dx, head_dy, distance in moves:
        for _ in range(distance):
            positions[0][0] += head_dx
            positions[0][1] += head_dy
            for segment_index in range(1, snek_size):
                update_snek(positions[segment_index], positions[segment_index - 1])

            all_tail_coords.add(tuple(positions[-1]))
            # print_snek(positions)

    # print_snek(list(all_tail_coords), show_numbers=False)
    return all_tail_coords


moves = load_moves()

# part 1
print(f"Part 1 solution: {len(snek(2, moves))}")

# part 2
print(f"Part 2 solution: {len(snek(10, moves))}")
