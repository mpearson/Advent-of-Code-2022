from pathlib import Path
from dataclasses import dataclass
import numpy as np

data_path = "data/problem_19.txt"
data_path = "data/problem_19_test.txt"

@dataclass
class Blueprint:
    index: int
    # bot order is [ore, clay, obsidian, geode]
    bot_costs: np.ndarray

    @classmethod
    def from_text(cls, line):
        line = line.split(" ")
        return cls(
            index=int(line[1][:-1]),
            bot_costs=np.array((
                (int(line[6]), 0, 0, 0),
                (int(line[12]), 0, 0, 0),
                (int(line[18]), int(line[21]), 0, 0),
                (int(line[27]), 0, int(line[30]), 0),
            ))
        )


with open(data_path, "r") as f:
    blueprints = [Blueprint.from_text(line) for line in f]

# for b in blueprints:
#     print(b)

class RobotSimulator:
    def __init__(self):
        self.bot_counts = np.array([1, 0, 0, 0])
        self.resources = np.array([0, 0, 0, 0])
        self.manufactured = np.array([0, 0, 0, 0])

        self.sim_count = 0

    def do_the_robot(self, blueprint, bot_sequence):
        self.sim_count += 1
        if self.sim_count % 1000 == 0:
            print(f"Scenario {self.sim_count}")
        # print(blueprint)
        # print(f"testing sequence: {bot_sequence}")
        self.bot_counts[:] = (1, 0, 0, 0)
        self.resources[:] = 0
        self.manufactured[:] = 0
        bot_sequence2 = bot_sequence
        bot_sequence = iter(bot_sequence)
        next_bot_type = next(bot_sequence)

        for i in range(24):
            if np.all(self.resources >= blueprint.bot_costs[next_bot_type]):
                self.resources -= blueprint.bot_costs[next_bot_type]
                self.manufactured[next_bot_type] = 1
                next_bot_type = next(bot_sequence)

            self.resources += self.bot_counts
            self.bot_counts += self.manufactured
            self.manufactured[:] = 0
            # print(f"Minute {i + 1}: bot_counts={bot_counts.tolist()}, resources={resources.tolist()}")

        return self.resources[3]

    def find_optimal_sequence(self, blueprint, sequence, max_bot_type):
        if len(sequence) == 11:
            try:
                return self.do_the_robot(blueprint, sequence)
            except StopIteration:
                return self.resources[3]  # hacky but whatever

        max_geodes = 0
        # we can only build one bot beyond the current "tech level".
        # let's try starting with the highest level bot
        for bot_type in range(max_bot_type, -1, -1):
            max_bot_type = min(bot_type + 1, 3)
            max_geodes = max(max_geodes, self.find_optimal_sequence(blueprint, sequence + [bot_type], max_bot_type))

        return max_geodes


# part 1
sim = RobotSimulator()
max_geodes = 0
optimal_blueprint = None
for blueprint in blueprints:
    geodes = sim.find_optimal_sequence(blueprint, [], 1)
    if geodes > max_geodes:
        max_geodes = geodes
        optimal_blueprint = blueprint.index

print(f"max_geodes: {max_geodes}")
print(f"optimal_blueprint: {optimal_blueprint}")


# geodes = sim.do_the_robot(blueprints[0], [1, 1, 1, 2, 1, 2, 3, 3, 3])
print(f"Part 1 solution: {optimal_blueprint}")

# part 2
print(f"Part 2 solution: {None}")

