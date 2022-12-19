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
    directions = enumerate(iter_loop(directions))
    blocks = iter_loop(blocks)
    game_board = np.zeros((4 * number_of_blocks, board_width), dtype=int)

    highest_obstacle = 0
    for i in range(number_of_blocks):
        block_x = 2
        block_y = highest_obstacle + 3
        block = next(blocks)
        while True:
            direction_index, dx = next(directions)
            if not check_collision(game_board, block, block_x + dx, block_y):
                block_x += dx

            if not check_collision(game_board, block, block_x, block_y - 1):
                block_y -= 1
            else:
                draw_block(game_board, block, block_x, block_y, 1)
                # Determine the height of the tallest column. Yes it's ugly, I don't wanna talk about it
                zeros_per_column = np.argmax(game_board[::-1] != 0, axis=0)
                highest_obstacle = game_board.shape[0] - zeros_per_column[zeros_per_column != 0].min()
                break

    return highest_obstacle


# # part 1
print(f"Part 1 solution: {play_tetris(jet_directions, tetris_blocks, 2022)}")
# print(f"Part 1 solution: {play_tetris(jet_directions, tetris_blocks, 30)}")

# # part 2
# print(f"Part 2 solution: {None}")

