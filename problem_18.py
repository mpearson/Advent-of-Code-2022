from pathlib import Path
from collections import deque
import numpy as np

data_path = "data/problem_18.txt"
# data_path = "data/problem_18_test.txt"

indices = np.genfromtxt(data_path, dtype=np.uint8, delimiter=",")
data_cube = np.zeros(indices.max(axis=0) + 3, dtype=int)  # need some padding so the most extreme surfaces get counted
data_cube[indices[:, 0] + 1, indices[:, 1] + 1, indices[:, 2] + 1] = 1

def get_surface_area(array):
    return sum([np.sum(np.abs(np.diff(array, axis=i))) for i in range(3)])


def get_neighbors(coords, shape):
    # yioeld all non-diagonal neighbors in all dimensions
    for axis, dim_size in enumerate(shape):
        neighbor_coords = list(coords)
        if coords[axis] + 1 < dim_size:
            neighbor_coords[axis] = coords[axis] + 1
            yield tuple(neighbor_coords)

        if coords[axis] > 0:
            neighbor_coords[axis] = coords[axis] - 1
            yield tuple(neighbor_coords)


def flood_fill(array, seed_coords, new_value):
    seed_value = array[seed_coords]
    if seed_value == new_value:
        return
    open_set = [seed_coords]
    while open_set:
        next_open_set = []
        for coords in open_set:
            for n in get_neighbors(coords, array.shape):
                if array[n] == seed_value:
                    array[n] = new_value
                    next_open_set.append(n)
        open_set = next_open_set


# part 1
surface_area = get_surface_area(data_cube)
print(f"Part 1 solution: {surface_area}")

# part 2
flood_fill(data_cube, (0, 0, 0), 1)
inner_surface_area = get_surface_area(data_cube)
print(f"Part 2 solution: {surface_area - inner_surface_area}")
