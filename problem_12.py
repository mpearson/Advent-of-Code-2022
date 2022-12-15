import sys
import heapq
import dataclasses
from pathlib import Path
import numpy as np

data_path = "data/problem_12.txt"
# data_path = "data/problem_12_test.txt"


def load():
    with open(data_path, "rb") as f:
        data = np.fromfile(f, dtype=np.uint8, sep="")

    width = np.argmax(data == ord("\n"))
    data = data.reshape(-1, width + 1)[:, :-1].astype(np.int32)

    start = divmod(np.argmax(data == ord("S")), width)
    end = divmod(np.argmax(data == ord("E")), width)
    print(f"start: {start}")
    print(f"end: {end}")

    data[start[0], start[1]] = ord("a")
    data[end[0], end[1]] = ord("z")

    data -= data.min()

    return data, start, end


@dataclasses.dataclass
class GraphNode:
    y: int
    x: int

    # The height, used exclusively to determine connectivity
    height: int

    # The minimum cost to get to the end from this node.This distance is the sum of all node
    # values along the cheapest path to the end.
    distance: int = sys.maxsize

    # Whether the node has been discovered. Could use distance but it turns out the int comparison
    # of `distance == sys.maxsize` is significantly slower than using this flag. With the flag, the
    # initial distance value doesn't matter.
    discovered: bool = False

    neighbors: list = None

    def compute_neighbors(self, grid):
        self.neighbors = []
        # south
        if self.y + 1 < grid.shape[0]:
            self.neighbors.append(grid[self.y + 1, self.x])
        # north
        if self.y > 0:
            self.neighbors.append(grid[self.y - 1, self.x])
        # east
        if self.x + 1 < grid.shape[1]:
            self.neighbors.append(grid[self.y, self.x + 1])
        # west
        if self.x > 0:
            self.neighbors.append(grid[self.y, self.x - 1])

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        return self.distance < other.distance


def create_nodes(height_grid):

    # Build a 2D array of nodes so we can easily look them up by coordinates
    node_grid = np.empty_like(height_grid, dtype=object)
    for y in range(height_grid.shape[0]):
        for x in range(height_grid.shape[1]):
            node_grid[y, x] = GraphNode(y, x, height_grid[y, x])

    for node in node_grid.flatten():
        node.compute_neighbors(node_grid)# = list(node.get_neighbors(node_grid))

    return node_grid


def print_dense_grid(array):
    for row in array:
        print("".join([str(x) for x in row]))


def print_grid_distances(node_grid):
    def format_node(node):
        if node.discovered:
            return f"{node.distance}".rjust(4)
        return "  ? "

    print("   |" + "".join([str(i).rjust(4) for i in range(node_grid.shape[1])]))
    print("---+-" + ("-" * (5 * node_grid.shape[1])))
    for i, node_row in enumerate(node_grid):
        print(str(i).ljust(3) + "| " + "".join([format_node(node) for node in node_row]))


def print_path(node_grid, path):
    if path is None:
        print("Dangit")
        return

    def format_height(height):
        if height < 0:
            return f"[{str(-height)}]".rjust(4)
        else:
            return f" {str(height)} ".rjust(4)

    path_grid = np.zeros_like(node_grid, dtype=np.int32)
    path_grid[...] = np.array([node.height for node in node_grid.flatten()]).reshape(path_grid.shape)

    for node in path:
        path_grid[node.y, node.x] = -node.distance

    print("   |" + "".join([str(i).rjust(4) for i in range(path_grid.shape[1])]))
    print("---+-" + ("-" * (4 * path_grid.shape[1])))
    for i, height_row in enumerate(path_grid):
        print(str(i).ljust(3) + "| " + "".join([format_height(height) for height in height_row]))


def compute_distances(node_grid, start_node, end_node):
    # The distance for the destination is simply the cost of the end node itself.
    end_node.discovered = True
    end_node.distance = 1

    # The initial open set is simply the starting node.
    open_set = [end_node]
    heapq.heapify(open_set)

    # print(f"Initial state:")
    # print_grid_distances(node_grid)

    for i in range(1000000):
        if len(open_set) == 0:
            print("Ran out of nodes to explore")
            break

        current_node = heapq.heappop(open_set)

        for neighbor in current_node.neighbors:
            if current_node.height - neighbor.height > 1:
                continue
            if not neighbor.discovered:
                neighbor.discovered = True
                neighbor.distance = current_node.distance + 1
                heapq.heappush(open_set, neighbor)
            else:
                pass

        if current_node is start_node:
            print(f"Path found! iteration: {i}, distance: {current_node.distance}")
            return

        # print(f"Iteration {i}, open set size = {len(open_set)}:")
        # print_grid_distances(node_grid)


def find_optimal_path(node_grid, start_node, end_node):
    path = [start_node]
    current_node = start_node

    for i in range(10000):
        current_neighbors = [n for n in current_node.neighbors if n.height - current_node.height <= 1]
        current_node = min(current_neighbors, key=lambda node: node.distance)
        path.append(current_node)
        if current_node is end_node:
            return list(reversed(path))

    return None


# part 1
data, start, end = load()
# print(data)
node_grid = create_nodes(data)
start_node = node_grid[start[0], start[1]]
end_node = node_grid[end[0], end[1]]
compute_distances(node_grid, start_node, end_node)
# print_grid_distances(node_grid)

optimal_path = find_optimal_path(node_grid, start_node, end_node)
# print_path(node_grid, optimal_path)

print(f"Part 1 solution: {len(optimal_path) - 1}")

# part 2

node_grid = create_nodes(data)
end_node = node_grid[end[0], end[1]]
compute_distances(node_grid, None, end_node)  # explore the entire grid, no start node
# print_grid_distances(node_grid)

# find node with height "a" that has the lowest distance to the end node
start_node = None
for node in node_grid.flatten():
    if node.discovered and node.height == 0 and (start_node is None or node.distance < start_node.distance):
        start_node = node

optimal_path = find_optimal_path(node_grid, start_node, end_node)
# print_path(node_grid, optimal_path)

print(f"Part 2 solution: {len(optimal_path) - 1}")

