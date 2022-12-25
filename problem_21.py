from pathlib import Path
import dataclasses
import numpy as np

data_path = "data/problem_21.txt"
# data_path = "data/problem_21_test.txt"


@dataclasses.dataclass
class MonkeyNode:
    name: str
    number: int = None
    listener: "MonkeyNode" = None

    operator: str = None
    monkey_1: "MonkeyNode" = None
    monkey_2: "MonkeyNode" = None
    dependent: bool = False

    @classmethod
    def from_text(cls, line):
        tokens = line.rstrip().split(" ")
        name = tokens[0][:-1]
        if len(tokens) == 2:
            return cls(name, number=int(tokens[1]))
        else:
            assert len(tokens) == 4
            return cls(name, operator=tokens[2], monkey_1=tokens[1], monkey_2=tokens[3])


def load():
    with open(data_path, "r") as f:
        monkeys = [MonkeyNode.from_text(line) for line in f]

    monkey_dict = {monkey.name: monkey for monkey in monkeys}

    for monkey in monkeys:
        if monkey.number is None:
            monkey.monkey_1 = monkey_dict[monkey.monkey_1]
            monkey.monkey_2 = monkey_dict[monkey.monkey_2]
            assert monkey.monkey_1.listener is None
            assert monkey.monkey_2.listener is None
            monkey.monkey_1.listener = monkey
            monkey.monkey_2.listener = monkey

    return monkey_dict

monkey_dict = load()

# part 1
def do_the_monkey(monkey):
    if monkey.number is None:
        monkey_1_value = do_the_monkey(monkey.monkey_1)
        monkey_2_value = do_the_monkey(monkey.monkey_2)

        match monkey.operator:
            case "+":
                return monkey_1_value + monkey_2_value
            case "-":
                return monkey_1_value - monkey_2_value
            case "*":
                return monkey_1_value * monkey_2_value
            case "/":
                return monkey_1_value // monkey_2_value

    return monkey.number

print(f"Part 1 solution: {do_the_monkey(monkey_dict['root'])}")

# part 2
monkey_dict["root"].operator = "="
monkey_dict["humn"].number = None

def mark_dependent_monkeys(monkey):
    monkey.dependent = True
    if monkey.listener is not None:
        mark_dependent_monkeys(monkey.listener)

mark_dependent_monkeys(monkey_dict["humn"])

def become_the_monkey(monkey, target_value):
    assert monkey.number is None
    if monkey.name == "humn":
        return target_value

    if monkey.monkey_1.dependent:
        dependent_monkey = monkey.monkey_1
        independent_monkey = monkey.monkey_2
    else:
        dependent_monkey = monkey.monkey_2
        independent_monkey = monkey.monkey_1

    match monkey.operator:
        case "+":
            # target = monkey_1 + monkey_2
            return become_the_monkey(dependent_monkey, target_value - do_the_monkey(independent_monkey))
        case "-":
            # target = monkey_1 - monkey_2
            if monkey.monkey_1 is dependent_monkey:
                return become_the_monkey(dependent_monkey, target_value + do_the_monkey(independent_monkey))
            else:
                return become_the_monkey(dependent_monkey, do_the_monkey(independent_monkey) - target_value)
        case "*":
            # target = monkey_1 * monkey_2
            return become_the_monkey(dependent_monkey, target_value // do_the_monkey(independent_monkey))
        case "/":
            # target = monkey_1 // monkey_2
            if monkey.monkey_1 is dependent_monkey:
                return become_the_monkey(dependent_monkey, target_value * do_the_monkey(independent_monkey))
            else:
                return become_the_monkey(dependent_monkey, do_the_monkey(independent_monkey) // target_value)
        case "=":
            # target = monkey_1 == monkey_2
            return become_the_monkey(dependent_monkey, do_the_monkey(independent_monkey))

print(f"Part 2 solution: {become_the_monkey(monkey_dict['root'], 1)}")
