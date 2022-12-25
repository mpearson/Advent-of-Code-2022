from pathlib import Path
import numpy as np

data_path = "data/problem_20.txt"
# data_path = "data/problem_20_test.txt"

data = np.genfromtxt(data_path, dtype=np.int64)

def mix_this_shit(numbers, indices):
    for original_index in range(len(indices)):
        current_index = indices[original_index]
        value = numbers[current_index]
        new_index = (current_index + value) % (len(numbers) - 1)
        if new_index > current_index:
            numbers[current_index : new_index] = numbers[current_index + 1 : new_index + 1]
            numbers[new_index] = value

            # find all the original values that ended up in this range,
            # and decrement them by 1 since they've all shifted left
            indices[(indices >= current_index) & (indices <= new_index)] -= 1
            indices[original_index] = new_index

        elif new_index < current_index:
            numbers[new_index + 1 : current_index + 1] = numbers[new_index : current_index]
            numbers[new_index] = value

            # find all the original values that ended up in this range,
            # and increment them by 1 since they've all shifted right
            indices[(indices >= new_index) & (indices <= current_index)] += 1
            indices[original_index] = new_index

        else:
            # Value is either 0, or it has wrapped around back to it's current location.
            # Either way nothing needs to be done
            pass

        # print(f"moved {value}", numbers, indices)

# part 1
numbers = data.copy()
zero_index = np.argmax(numbers == 0)
indices = np.arange(len(numbers), dtype=np.int32)
mix_this_shit(numbers, indices)

coordinates = numbers[(np.arange(1000, 4000, 1000) + indices[zero_index]) % len(numbers)]
print(f"Part 1 solution: {coordinates.sum()}")

# part 2
numbers = data.copy() * 811589153
zero_index = np.argmax(numbers == 0)
indices = np.arange(len(numbers), dtype=np.int32)

for round_index in range(10):
    mix_this_shit(numbers, indices)

# print(numbers)
coordinates = numbers[(np.arange(1000, 4000, 1000) + indices[zero_index]) % len(numbers)]


print(f"Part 2 solution: {coordinates.sum()}")
