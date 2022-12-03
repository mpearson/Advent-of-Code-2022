from pathlib import Path

for i in range(2, 26):
    with open(f"problem_{i:02d}.py", "w") as f:
        f.write(f"""from pathlib import Path
import numpy as np

data_path = "data/problem_{i:02d}.txt"
# data_path = "data/problem_{i:02d}_test.txt"

# print(data)

# part 1
print(f"Part 1 solution: {{None}}")

# part 2
print(f"Part 2 solution: {{None}}")

""")

    with open(f"data/problem_{i:02d}.txt", "w+") as f:
        pass
    with open(f"data/problem_{i:02d}_test.txt", "w+") as f:
        pass

