from pathlib import Path
import numpy as np

data_path = "data/problem_08.txt"
# data_path = "data/problem_08_test.txt"


CHAR_OFFSET = ord("0")

with open(data_path, "r") as f:
    rows = []
    for line in f:
        rows.append([ord(c) - CHAR_OFFSET for c in line[:-1]])
    tree_height = np.array(rows)


def get_slice(axis, axis_slice):
    if axis == 0:
        return (axis_slice, slice(1, -1))
    return (slice(1, -1), axis_slice)


def propagate_visibility(visibility, axis, reverse):
    """Update visibility from one of the 4 directions."""
    if reverse:
        offset_sequence = range(tree_height.shape[0] - 1, -1, -1)
    else:
        offset_sequence = range(0, tree_height.shape[0], 1)

    highest_obstacle = tree_height[get_slice(axis, offset_sequence[0])].copy()

    for offset in offset_sequence[1:]:
        offset_slice = get_slice(axis, offset)
        visibility[offset_slice] |= tree_height[offset_slice] > highest_obstacle
        highest_obstacle[:] = np.maximum(
            tree_height[offset_slice],
            highest_obstacle
        )


# part 1
visibility = np.ones_like(tree_height, dtype=bool)
visibility[1:-1, 1:-1] = 0
for axis, reverse in ((0, False), (0, True), (1, False), (1, True)):
    propagate_visibility(visibility, axis, reverse)

propagate_visibility(visibility, 0, 1)
propagate_visibility(visibility, 0, -1)
propagate_visibility(visibility, 1, 1)
propagate_visibility(visibility, 1, -1)

print("\ntree_height:")
print(tree_height[:10, :10])
print("\nvisibilty:")
print(visibility[:10, :10])

print(f"Part 1 solution: {visibility.sum()}")


# part 2
def look_out_the_winder(height_map, axis, reverse):
    distance = np.zeros_like(height_map)

    if reverse:
        offset_sequence = range(distance.shape[axis] - 2, 0, -1)
    else:
        offset_sequence = range(1, distance.shape[axis] - 1, 1)

    for offset in offset_sequence:
        offset_slice = get_slice(axis, slice(offset, offset +1))
        if reverse:
            view_direction_slice = get_slice(axis, slice(offset - 1, -distance.shape[axis] - 1, -1))
        else:
            view_direction_slice = get_slice(axis, slice(offset + 1, None, 1))

        view_distance_from_offset = np.argmax(
            height_map[view_direction_slice] >= height_map[offset_slice],
            axis=axis
        ) + 1

        distance[offset_slice] = np.expand_dims(view_distance_from_offset, axis)

    return distance


def look_out_every_winder(height_map):
    # view distance needs to stop at the edge regardless of your height
    # this is also necessary because np.argmax() returns 0 if the condition is never met,
    # which screws up the math. Large edge values guarantees the condition is met eventually
    height_map = height_map.copy()
    height_map[0, :] = 9
    height_map[-1, :] = 9
    height_map[:, 0] = 9
    height_map[:, -1] = 9

    scenic_score = np.ones_like(height_map)
    for axis, reverse in ((0, False), (0, True), (1, False), (1, True)):
        scenic_score *= look_out_the_winder(height_map, axis, reverse)

    return scenic_score


scenic_score = look_out_every_winder(tree_height)

print("\nscenic_score:")
print(scenic_score[:10, :10])

print(f"Part 2 solution: {scenic_score.max()}")

