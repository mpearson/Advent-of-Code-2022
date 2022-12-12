import json
import dataclasses
from pathlib import Path
from collections import deque
import numpy as np

data_path = "data/problem_11.txt"
# data_path = "data/problem_11_test.txt"


class WorryLevel:
    def __init__(self, raw_value, divisors):
        self.raw_value = raw_value
        self.moduli = divisors
        self.modular_values = [raw_value % modulus for modulus in self.moduli]
        self.modular_values = [raw_value] * len(self.moduli)

    def operate(self, operator, rhs_value):
        for index, modulus in enumerate(self.moduli):
            current_value = self.modular_values[index]
            if rhs_value is None:
                modular_rhs_value = current_value
            else:
                modular_rhs_value = rhs_value
            if operator == "+":
                self.modular_values[index] = (current_value + modular_rhs_value) % modulus
            elif operator == "*":
                self.modular_values[index] = (current_value * modular_rhs_value) % modulus
            else:
                raise Exception(f"wat: {self.operator}")

    def operate_naive(self, operator, rhs_value):
        current_value = self.raw_value
        if rhs_value is None:
            rhs_value = self.raw_value
        if operator == "+":
            self.raw_value = self.raw_value + rhs_value
        elif operator == "*":
            self.raw_value = self.raw_value * rhs_value
        elif operator == "/":
            self.raw_value = self.raw_value // rhs_value
        else:
            raise Exception(f"wat: {self.operator}")

    def is_divisible(self, divisor_index):
        return self.modular_values[divisor_index] == 0

    def is_divisible_naive(self, divisor):
        return self.raw_value % divisor == 0

    def apply_xanax(self):
        # well that's one way to reduce "worry levels" right?
        self.operate_naive("/", 3)


@dataclasses.dataclass
class Monkey:
    monkey_index: int = None
    items: list[int | WorryLevel] = None
    operator: str = None
    operation_value: str | int = None
    divisor: int = None
    monkey_if_true: int = None
    monkey_if_false: int = None
    monkey_roster: int = None
    item_fondle_count: int = 0
    enable_xanax: bool = True

    def set_monkeys(self, monkey_roster):
        """Replace each value with a WorryLevel instance and populate its modular arithmetic shit."""
        self.monkey_roster = monkey_roster
        divisors = [monkey.divisor for monkey in monkey_roster]
        self.items = [WorryLevel(raw_value, divisors) for raw_value in self.items]

    def do(self):
        for item in self.items:
            self.item_fondle_count += 1
            if self.enable_xanax:
                item.operate_naive(self.operator, self.operation_value)
                item.apply_xanax()
                is_divisible = item.is_divisible_naive(self.divisor)
            else:
                item.operate(self.operator, self.operation_value)
                is_divisible = item.is_divisible(self.monkey_index)

            next_monkey_index = self.monkey_if_true if is_divisible else self.monkey_if_false
            self.monkey_roster[next_monkey_index].items.append(item)

        self.items.clear()


def compute_monkey_business(rounds, enable_xanax=True):
    monkey_roster = []
    with open(data_path, "r") as f:
        for line in f:
            if line.startswith("Monkey"):
                monkey = Monkey()
                monkey.monkey_index = int(line[7:-2])
                monkey.items = [int(item) for item in next(f)[18:].split(", ")]
                monkey.operator, monkey.operation_value = next(f)[23:-1].split(" ")
                if monkey.operation_value == "old":
                    monkey.operation_value = None
                else:
                    monkey.operation_value = int(monkey.operation_value)
                monkey.divisor = int(next(f)[21:-1])
                monkey.monkey_if_true = int(next(f)[29:-1])
                monkey.monkey_if_false = int(next(f)[30:-1])
                monkey_roster.append(monkey)

    for monkey in monkey_roster:
        monkey.enable_xanax = enable_xanax
        monkey.set_monkeys(monkey_roster)

    for i in range(rounds):
        for monkey in monkey_roster:
            monkey.do()

    fondling_levels = [monkey.item_fondle_count for monkey in monkey_roster]
    print(fondling_levels)
    fondling_levels.sort()
    return fondling_levels[-1] * fondling_levels[-2]


# part 1
print(f"Part 1 solution: {compute_monkey_business(20)}")


# part 2
print(f"Part 2 solution: {compute_monkey_business(10000, enable_xanax=False)}")
