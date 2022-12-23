from pathlib import Path
import numpy as np

data_path = "data/problem_17.txt"
# data_path = "data/problem_17_test.txt"

jet_directions = (np.fromfile(data_path, dtype=np.uint8)[:-1] == ord(">")) * 2 - 1

tetris_blocks = [np.array(block) for block in (
    [[1, 1, 1, 1]],  # 1x4 horizontal

    [[0, 1, 0],  # 3x3 "+"
     [1, 1, 1],
     [0, 1, 0]],

    [[1, 1, 1],  # 3x3 mirrored "L". Note it's also flipped because of...reasons
     [0, 0, 1],  # (jk it's because I'm using +Y for up)
     [0, 0, 1]],

    [[1],  # 4x1 vertical
     [1],
     [1],
     [1]],

    [[1, 1],  # 2x2 square
     [1, 1]],
)]

def iter_loop(iterable, notify=False):
    while True:
        yield from iterable
        if notify:
            print("ding")

def draw_block(game_board, block, block_x, block_y, value):
    game_board[
        block_y : block_y + block.shape[0],
        block_x : block_x + block.shape[1]
    ] += block * value

    game_board[game_board > 2] = value

def check_collision(game_board, block, block_x, block_y):
    # if block_x < 0 or block_x + block.shape[1] >= game_board.shape[1]

    return block_y < 0 or block_x < 0 or block_x + block.shape[1] > game_board.shape[1] or np.any(
        game_board[
            block_y : block_y + block.shape[0],
            block_x : block_x + block.shape[1]
        ] * block
    )

def print_board(game_board, preview_height, block=None, block_x=None, block_y=None):
    preview_height = max(preview_height, 8)
    if block is not None:
        preview_height = max(preview_height, block_y + block.shape[0])

    truncated_board = game_board[:preview_height].copy()

    if block is not None:
        draw_block(truncated_board, block, block_x, block_y, 2)

    chars = ".#@"
    for row in truncated_board[::-1]:
        print("".join([chars[value] for value in row]))
    print()

def play_tetris(directions, blocks, number_of_blocks, board_width=7):
    directions = enumerate(iter_loop(directions, True))
    blocks = iter_loop(blocks)
    game_board = np.zeros((4 * number_of_blocks, board_width), dtype=int)
    # heights = [(0, 0)]
    highest_obstacle = 0
    for i in range(number_of_blocks):
        # print(f"Rock {i}")
        # print(f"highest_obstacle: {highest_obstacle}")
        block_x = 2
        block_y = highest_obstacle + 3
        block = next(blocks)
        # print_board(game_board, highest_obstacle, block, block_x, block_y)
        while True:
            direction_index, dx = next(directions)
            # print(f"move: {'right' if dx == 1 else 'left'}")
            if not check_collision(game_board, block, block_x + dx, block_y):
                block_x += dx

            if not check_collision(game_board, block, block_x, block_y - 1):
                block_y -= 1
            else:
                draw_block(game_board, block, block_x, block_y, 1)
                # Determine the height of the tallest column. Yes it's ugly, I don't wanna talk about it
                zeros_per_column = np.argmax(game_board[::-1] != 0, axis=0)
                highest_obstacle = game_board.shape[0] - zeros_per_column[zeros_per_column != 0].min()
                # heights.append((highest_obstacle, block.shape[0]))
                # print_board(game_board, highest_obstacle)
                break
                # print_board(game_board, highest_obstacle, block, block_x, block_y)

    # print(direction_index - direction_count)
    return highest_obstacle#, heights

# print(jet_directions)
# print(len(jet_directions))

# a = np.array([
#     [0, 1, 1, 0],
#     [0, 0, 1, 0],
#     [0, 0, 1, 1],
#     [0, 0, 0, 1],
#     [0, 0, 2, 1],
#     [0, 0, 1, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
# ])

# # highest_obstacle = a.shape[0] - np.argmax(a[::-1] != 0, axis=0) - 1
# zeros_per_column = np.argmax(a[::-1] != 0, axis=0)
# print(zeros_per_column)

# highest_obstacle = a.shape[0] - zeros_per_column[zeros_per_column != 0].min() - 1
# # highest_obstacle = a.shape[0] - np.argmax(a[::-1] != 0, axis=0)[a[0] != 0].min() - 1

# print(a)
# print()
# print(highest_obstacle)



# # disable truncating numpy arrays
# np.set_printoptions(threshold=np.inf)

# highest, heights = play_tetris(jet_directions, tetris_blocks, 5000)

# # slope = heights[-1] / len(heights)
# # estimates = np.arange(0, heights[-1], slope).astype(int)
# # print(np.diff(heights))
# # print(heights - estimates)
# heights = np.array(heights)
# print(heights[1:, 1] - np.diff(heights[:, 0]))  # how much did the increase in total height differ from the block's height?

# y = heights
# x = np.arange(len(heights))

# # fit straight line to y(x)
# m, b = np.polyfit(x, y, 1)
# print(m, b)

# estimates = (m * x + b).astype(int)

# print(heights - estimates)

# # part 1
print(f"Part 1 solution: {play_tetris(jet_directions, tetris_blocks, 2022)}")
# print(f"Part 1 solution: {play_tetris(jet_directions, tetris_blocks, 30)}")

# # part 2
# print(f"Part 2 solution: {None}")

