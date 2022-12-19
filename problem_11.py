import json
import dataclasses
from pathlib import Path

data_path = "data/problem_11.txt"
# data_path = "data/problem_11_test.txt"


class WorryLevel:
    def __init__(self, raw_value):
        self.raw_value = raw_value
        self.modulus = None
        self.value = None

    def set_modulus(self, modulus):
        self.modulus = modulus
        self.value = self.raw_value % self.modulus

    def operate(self, operator, rhs_value):
        if rhs_value is None:
            rhs_value = self.value
        if operator == "+":
            self.value = (self.value + rhs_value) % self.modulus
        elif operator == "*":
            self.value = (self.value * rhs_value) % self.modulus
        elif operator == "/":
            self.value = self.value // rhs_value
        else:
            raise Exception(f"wat: {self.operator}")

    def is_divisible(self, divisor):
        return self.value % divisor == 0

    def apply_xanax(self):
        # well that's one way to reduce "worry levels" right?
        self.operate("/", 3)


@dataclasses.dataclass
class Monkey:
    monkey_index: int = None
    items: list[WorryLevel] = None
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
        modulus = 1
        for monkey in monkey_roster:
            modulus *= monkey.divisor
        for item in self.items:
            item.set_modulus(modulus)

    def do(self):
        for item in self.items:
            self.item_fondle_count += 1
            item.operate(self.operator, self.operation_value)
            if self.enable_xanax:
                item.apply_xanax()
            next_monkey_index = self.monkey_if_true if item.is_divisible(self.divisor) else self.monkey_if_false
            self.monkey_roster[next_monkey_index].items.append(item)

        self.items.clear()


def compute_monkey_business(rounds, enable_xanax=True):
    monkey_roster = []
    with open(data_path, "r") as f:
        for line in f:
            if line.startswith("Monkey"):
                monkey = Monkey()
                monkey.monkey_index = int(line[7:-2])
                monkey.items = [WorryLevel(int(item)) for item in next(f)[18:].split(", ")]
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
