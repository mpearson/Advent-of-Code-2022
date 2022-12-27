from pathlib import Path

for i in range(22, 26):
    with open(f"problem_{i:02d}.py", "w", newline="\n") as f:
        f.write(f"""from pathlib import Path
import numpy as np

data_path = "data/problem_{i:02d}.txt"
# data_path = "data/problem_{i:02d}_test.txt"


# data = np.genfromtxt(data_path, dtype=np.int32)

# with open(data_path, "r") as f:
#     data = f.readlines()

# print(data)

# part 1
print(f"Part 1 solution: {{None}}")

# part 2
print(f"Part 2 solution: {{None}}")

""")

    with open(f"data/problem_{i:02d}.txt", "w+", newline="\n") as f:
        pass
    with open(f"data/problem_{i:02d}_test.txt", "w+", newline="\n") as f:
        pass

