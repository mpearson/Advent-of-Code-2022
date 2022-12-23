import re
from pathlib import Path
import numpy as np

data_path = "data/problem_15.txt"
# data_path = "data/problem_15_test.txt"


FILE_REGEX = re.compile(r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)")

def load():
    with open(data_path, "r") as f:
        sensor_pos = []
        beacon_pos = []
        for line in f:
            results = FILE_REGEX.match(line.strip())
            sensor_x = int(results[1])
            sensor_y = int(results[2])
            beacon_x = int(results[3])
            beacon_y = int(results[4])

            sensor_pos.append((sensor_x, sensor_y))
            beacon_pos.append((beacon_x, beacon_y))

    return np.array(sensor_pos), np.array(beacon_pos)


def print_grid(grid):
    chars = ".BS#@"
    for index, row in enumerate(grid):
        # if index != 4:
        #     continue
        print("".join((chars[x] for x in row)))
    print()


# def print_exclusion_zone(grid, x, y, min_distance):
def print_exclusion_zone(grid, min_x, min_y, sensors, min_distances):
    grid = grid.copy()
    grid_y, grid_x = np.indices(grid.shape)
    for (sensor_x, sensor_y), min_distance in zip(sensors, min_distances):
        distance = np.abs(sensor_y - min_y - grid_y) + np.abs(sensor_x - min_x - grid_x)
        grid[(grid == 0) & (distance <= min_distance)] = 3
    # grid[y, x] = 4

    print_grid(grid)


def build_grid(sensor_pos, beacon_pos):
    min_x = min(sensor_pos[:, 0].min(), beacon_pos[:, 0].min())
    max_x = max(sensor_pos[:, 0].max(), beacon_pos[:, 0].max())
    min_y = min(sensor_pos[:, 1].min(), beacon_pos[:, 1].min())
    max_y = max(sensor_pos[:, 1].max(), beacon_pos[:, 1].max())

    grid = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=int)
    grid[beacon_pos[:, 1] - min_y, beacon_pos[:, 0] - min_x] = 1
    grid[sensor_pos[:, 1] - min_y, sensor_pos[:, 0] - min_x] = 2
    return grid, min_x, min_y


def ranges_overlap(a, b):
    return not ((a[0] > b[1] + 1) or (a[1] + 1 < b[0]))


def get_exclusion_zones_at_row(row_index, sensor_pos, min_distances):
    zone_ranges = []
    for (sensor_x, sensor_y), min_distance in zip(sensor_pos, min_distances):
        half_width = max(0, min_distance - abs(sensor_y - row_index))
        if half_width != 0:
            zone_ranges.append((sensor_x - half_width, sensor_x + half_width))

    return np.array(zone_ranges)


def merge_ranges(ranges):
    merged_ranges = ranges.tolist()
    disjoint_index = 0  # current number (minus 1) of disjoint sets identified
    while True:
        if disjoint_index >= len(merged_ranges) - 1:
            break

        overlap_found = False
        for i in range(1, len(merged_ranges)):
            if ranges_overlap(merged_ranges[disjoint_index], merged_ranges[i]):
                #
                overlap_found = True
                range_x, range_y = merged_ranges.pop(i)
                merged_ranges[disjoint_index] = (
                    min(merged_ranges[disjoint_index][0], range_x),
                    max(merged_ranges[disjoint_index][1], range_y),
                )
                break

        if not overlap_found:
            disjoint_index += 1

    return merged_ranges


def get_excluded_cells_at_row(row_index, sensor_pos, min_distances):
    zone_ranges = get_exclusion_zones_at_row(row_index, sensor_pos, min_distances)
    # zone_ranges = zone_ranges - zone_ranges[:, 0].min()

    # zone_ranges = np.array([
    #     [1, 10],
    #     [15, 20],
    #     [8, 15],
    #     [-20, -5],
    # ])
    # print(zone_ranges)

    zone_ranges = merge_ranges(zone_ranges)
    zone_ranges.sort(key=lambda zone_range: zone_range[0])
    # print(zone_ranges)

    return np.sum([end - start for start, end in zone_ranges])


sensor_pos, beacon_pos = load()
# grid, min_x, min_y = build_grid(sensor_pos, beacon_pos)
min_distances = (
    np.abs(sensor_pos[:, 0] - beacon_pos[:, 0]) +
    np.abs(sensor_pos[:, 1] - beacon_pos[:, 1])
)

# print(min_distances)
# for i in range(len(sensor_pos)):
#     print(f"Sensor {i}:")
#     print_exclusion_zone(grid, min_x, min_y, [sensor_pos[i]], [min_distances[i]])

# print_exclusion_zone(grid, min_x, min_y, sensor_pos, min_distances)
# print_grid(grid)


# part 1
print(f"Part 1 solution: {get_excluded_cells_at_row(2000000, sensor_pos, min_distances)}")

# part 2
def find_non_excluded_cell(sensor_pos, min_distances, max_coord):
    min_coord = 0
    for row_index in range(max_coord):
        if row_index % 1000 == 0:
            print(f"row {row_index}")
        zone_ranges = merge_ranges(get_exclusion_zones_at_row(row_index, sensor_pos, min_distances))
        for start, end in zone_ranges:
            if not (start <= min_coord and end >= max_coord):
                print(f"Possible location found in row {row_index}:")
                print(zone_ranges)
                break

# Note this takes several minutes, but unfortunately I have no interest in optimizing it.
# In real life you would probably use a quadtree or something.

# find_non_excluded_cell(sensor_pos, min_distances, 4000000)
# Possible location found in row 2638237:
# [(3270299, 4077403), (-589410, 3270297)]
y = 2638237
x = 3270298


print(f"Part 2 solution: {x * 4000000 + y}")
