from pathlib import Path
from dataclasses import dataclass
import numpy as np

data_path = "data/problem_21.txt"
# data_path = "data/problem_21_test.txt"


@dataclass
class MonkeyNode:

    name: str
    number: int = None
    operator: str = None


    @classmethod
    def from_text(cls, line):

        return cls()


with open(data_path, "r") as f:
    data = f.readlines()

# print(data)

# part 1
print(f"Part 1 solution: {None}")

# part 2
print(f"Part 2 solution: {None}")

# root: pppw + sjmn
# dbpl: 5
# cczh: sllz + lgvd
# zczc: 2
# ptdq: humn - dvpt
# dvpt: 3
# lfqf: 4
# humn: 5
# ljgn: 2
# sjmn: drzm * dbpl
# sllz: 4
# pppw: cczh / lfqf
# lgvd: ljgn * ptdq
# drzm: hmdt - zczc
# hmdt: 32
