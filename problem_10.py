from pathlib import Path
import numpy as np

data_path = "data/problem_10.txt"
# data_path = "data/problem_10_test.txt"

with open(data_path, "r") as f:
    data = f.read().splitlines()

register_values = [1]
for command in data:
    if command.startswith("addx"):
        value = int(command[5:])
        register_values.append(register_values[-1])
        register_values.append(register_values[-1] + value)
    else:
        assert command == "noop"
        register_values.append(register_values[-1])

register_values = np.array(register_values)
cycle_index = np.arange(1, len(register_values) + 1)
signal_values = register_values * cycle_index
signal_indices = np.array([20, 60, 100, 140, 180, 220]) - 1

# part 1
print(f"Part 1 solution: {signal_values[signal_indices].sum()}")

# part 2
def print_screen(buffer):
    chars = ".#"
    for row in buffer:
        print("".join(chars[value] for value in row))

screen_shape = (6, 40)
refresh_period = np.prod(screen_shape)
screen_buffer = np.zeros(screen_shape, dtype=int)
cycle_index = np.arange(refresh_period)
x_position = cycle_index % screen_shape[1]
screen_buffer.reshape(-1)[cycle_index] = np.abs(register_values[:refresh_period] - x_position) < 2

print(f"Part 2 solution:")
print_screen(screen_buffer)
