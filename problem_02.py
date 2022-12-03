from pathlib import Path
import numpy as np

data_path = "data/problem_02.txt"
# data_path = "data/problem_02_test.txt"

# part 1

SHAPE_SCORES = [1, 2, 3]
RESULT_SCORES = [0, 3, 6]  # draw, lose, win

# | a | b | result | (1 + a - b) % 3
# -----------------------------------
# | 0 | 0 | draw   |    1
# | 0 | 1 | lose   |    0
# | 0 | 2 | win    |    2
# |   |   |        |
# | 1 | 0 | win    |    2
# | 1 | 1 | draw   |    1
# | 1 | 2 | lose   |    0
# |   |   |        |
# | 2 | 0 | lose   |    0
# | 2 | 1 | win    |    2
# | 2 | 2 | draw   |    1

A_NUMERIC = ord("A")
X_NUMERIC = ord("X")

total_score = 0
with open(data_path, "r") as f:
    for line in f:
        opponent_move = ord(line[0]) - A_NUMERIC
        your_move = ord(line[2]) - X_NUMERIC
        result = (1 + your_move - opponent_move) % 3
        your_score = SHAPE_SCORES[your_move] + RESULT_SCORES[result]
        total_score += your_score
        # print(your_score)
print(f"Part 1 solution: {total_score}")

# part 2

# | b | strategy | a | (b - 1 + strat) % 3
# -------------------------------
# | 0 |    0     | 2 |  2
# | 0 |    1     | 0 |  0
# | 0 |    2     | 1 |  1

RESULT_SCORES = [0, 3, 6]  # lose, draw, win

total_score = 0
with open(data_path, "r") as f:
    for line in f:
        opponent_move = ord(line[0]) - A_NUMERIC
        your_strategy = ord(line[2]) - X_NUMERIC
        your_move = (opponent_move - 1 + your_strategy) % 3
        your_score = SHAPE_SCORES[your_move] + RESULT_SCORES[your_strategy]
        total_score += your_score
        # print(your_score)

print(f"Part 2 solution: {total_score}")

