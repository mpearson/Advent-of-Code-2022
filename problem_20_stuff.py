import numpy as np

data = np.array([1, 2, -3, 3, -2, 0, 4])
indices = np.arange(len(data), dtype=np.int32)


for original_index in range(len(indices)):
    current_index = indices[original_index]
    value = data[current_index]
    new_index = (current_index + value) % len(indices)




