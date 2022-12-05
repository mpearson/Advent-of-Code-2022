from pathlib import Path
import numpy as np

data_path = "data/problem_05.txt"
# data_path = "data/problem_05_test.txt"


def parse_initial_stacks(file_obj):
    rows = []
    number_of_cols = 0
    for line in file_obj:
        line = line.rstrip()
        if not line:
            # blank line after stacks, yay we're done
            break

        elif line[1] == "1":
            # pointless line of column numbers, skip
            continue
        else:
            # actual relevant line
            cols = list(line[1::4])

            number_of_cols = max(number_of_cols, len(cols))
            rows.append(cols)

    # right pad with empty values
    for index in range(len(rows)):
        row = rows[index]
        # rows[index] = row + [-1] * (number_of_cols - len(row))
        rows[index] = row + [" "] * (number_of_cols - len(row))

    rows = np.array(rows)[::-1].T
    return np.pad(rows, [(0, 0), (0, 50)], mode="constant", constant_values=" ")


def parse_move(line):
    move = [int(n) for n in line.split(" ")[1::2]]
    move[1] -= 1
    move[2] -= 1
    return move


def print_stacks(stacks):
    for row in stacks:
        print(" ".join(row.tolist()))


def move_crate(stacks, stack_heights, move, reverse):
    count, from_index, to_index = move
    # print(f"move {count} from {from_index} -> {to_index}")

    from_stack_height = stack_heights[from_index]
    to_stack_height = stack_heights[to_index]

    crates = stacks[from_index, from_stack_height - count : from_stack_height]
    if reverse:
        crates = crates[::-1]
    stacks[to_index, to_stack_height : to_stack_height + count] = crates
    stacks[from_index, from_stack_height - count : from_stack_height] = " "

    stack_heights[from_index] -= count
    stack_heights[to_index] += count


def get_answer(reverse):
    with open(data_path, "r") as f:
        stacks = parse_initial_stacks(f)
        stack_heights = (stacks != " ").sum(axis=1)

        for line in f:
            move = parse_move(line)
            move_crate(stacks, stack_heights, move, reverse)
            # print_stacks(stacks)

    top_crates = stacks[range(len(stacks)), stack_heights - 1]

    return "".join(top_crates.tolist())


# part 1
print(f"Part 1 solution: {get_answer(True)}")

# part 2
print(f"Part 2 solution: {get_answer(False)}")

