from pathlib import Path
import numpy as np

data_path = "data/problem_14.txt"
# data_path = "data/problem_14_test.txt"


SOURCE_POS_STUPID_COORDINATES = (500, 0)


def load():
    with open(data_path, "r") as f:
        data = f.readlines()

    contours = []
    min_x = max_x = SOURCE_POS_STUPID_COORDINATES[0]
    min_y = max_y = SOURCE_POS_STUPID_COORDINATES[1]
    for line in data:
        vertices = []
        for vertex in line.rstrip().split(" -> "):
            vertex = vertex.split(",")
            vertex = [int(vertex[0]), int(vertex[1])]
            vertices.append(vertex)
            min_x = min(min_x, vertex[0])
            max_x = max(max_x, vertex[0])
            min_y = min(min_y, vertex[1])
            max_y = max(max_y, vertex[1])

        contours.append(vertices)

    max_x -= min_x
    max_y -= min_y
    source_pos = [SOURCE_POS_STUPID_COORDINATES[0] - min_x, SOURCE_POS_STUPID_COORDINATES[1] - min_y]
    for vertices in contours:
        for vertex in vertices:
            vertex[0] -= min_x
            vertex[1] -= min_y

    shape = max_y + 1, max_x + 1
    return contours, source_pos, shape


def generate_grid(contours, grid_shape, source_pos, include_floor=False):
    if include_floor:
        # increase the grid size to include a 45° triangle beneath the sand source
        height = grid_shape[0] + 2
        width = 2 * height + 1
        x_offset = (width // 2) - source_pos[0]
        grid_shape = (height, width)
    else:
        x_offset = 0

    grid = np.zeros(grid_shape, dtype=int)
    if include_floor:
        grid[-1, :] = 1  # put in the floor

    for vertices in contours:
        for i in range(len(vertices) - 1):
            start_x, start_y = vertices[i]
            end_x, end_y = vertices[i + 1]
            if start_x == end_x:
                # vertical line
                grid[min(start_y, end_y) : max(start_y, end_y) + 1, start_x + x_offset] = 1
            elif start_y == end_y:
                # horizontal line
                grid[start_y, min(start_x, end_x) + x_offset : max(start_x, end_x) + 1 + x_offset] = 1
            else:
                raise ValueError(f"Aint nobody got time for diagonals! {vertices[i]} -> {vertices[i + 1]}")

    return grid, (source_pos[0] + x_offset, source_pos[1])


def print_grid(grid, source_pos):
    chars = ".#o"
    for row_index, row in enumerate(grid):
        row_chars = [chars[value] for value in row]

        if row_index == source_pos[1]:
            row_chars[source_pos[0]] = "+"

        print("".join(row_chars))


def drop_sand(grid, source_pos):
    """Move sand grain to final resting place, return True if this is off the map."""
    x, y = source_pos
    while True:
        if grid[y, x] == 2:  # dang ol thing is full
            return False

        if y >= grid.shape[0] - 1:  # dang ol thing is pouring off the edge
            return False

        if grid[y + 1, x] == 0:  # fall straight down
            y += 1
        elif grid[y + 1, x - 1] == 0:  # diagonal left
            y += 1
            x -= 1
        elif grid[y + 1, x + 1] == 0:  # diagonal right
            y += 1
            x += 1
        else:
            break  # nap time for sand

    grid[y, x] = 2
    return True


def drop_all_the_sand(grid, source_pos):
    count = 0
    while drop_sand(grid, source_pos):
        count += 1
        # if count % 10000 == 0:
        #     print(count)
        #     print_grid(grid, source_pos)

        if count > 1000000:  # just in case
            break
    return count


contours, source_pos, shape = load()
# print(contours)

# part 1
grid, source_pos = generate_grid(contours, shape, source_pos)
count = drop_all_the_sand(grid, source_pos)
print_grid(grid, source_pos)

print(f"Part 1 solution: {count}")

# part 2

# Note: since the non-filled regions end up being so small, the better way to do this would be to
# compute the area of the sand "shadows" under each stone cell, and the area occupied by the actual
# stones, and subtract that from a "perfect" pyramid. This would probably run 1000x faster,
# but as usual, developer time > cpu time
grid, source_pos = generate_grid(contours, shape, source_pos, include_floor=True)
count = drop_all_the_sand(grid, source_pos)
print_grid(grid, source_pos)
print(f"Part 2 solution: {count}")
