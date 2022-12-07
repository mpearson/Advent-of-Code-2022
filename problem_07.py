import json
from pathlib import Path
import dataclasses

import numpy as np

data_path = "data/problem_07.txt"
# data_path = "data/problem_07_test.txt"


@dataclasses.dataclass
class File:
    name: str
    size: int
    parent: "Directory" = None

    def to_dict(self):
        return dict(
            type="File",
            name=self.name,
            size=self.size
        )


@dataclasses.dataclass
class Directory:
    parent: "Directory" = None
    name: str = None
    size: int = None
    children: dict = dataclasses.field(default_factory=dict)

    def to_dict(self):
        return dict(
            name="[root]" if self.name == "" else self.name,
            type="Dir",
            size=self.size,
            children=[child.to_dict() for child in self.children.values()]
        )

    def compute_sizes(self):
        self.size = 0
        for child in self.children.values():
            if isinstance(child, File):
                self.size += child.size
            else:
                self.size += child.compute_sizes()
        return self.size

    def sum_small_dirs(self, size):

        small_dir_total = 0
        for child in self.children.values():
            if isinstance(child, Directory):
                small_dir_total += child.sum_small_dirs(size)

        # note that this counts directories twice
        if self.size <= size:
            small_dir_total += self.size
            # return self.size

        return small_dir_total

    def iter_subdirs(self):
        yield self
        for child in self.children.values():
            if isinstance(child, Directory):
                yield from child.iter_subdirs()


def get_new_cwd(cwd, destination):
    match destination:
        case "/":
            return Directory(name="")
        case "..":
            if cwd.parent is None:
                cwd.parent = Directory()

            assert cwd.name is not None
            assert cwd.parent.children.get(cwd.name) is cwd  # let's not bother with this case unless we need to
            return cwd.parent
        case dir_name:
            assert dir_name in cwd.children # is this always true? do we ever psychically
                                            # cd into a directory we've never seen?
                                            # only one way to find out...
            return cwd.children[dir_name]


def parse_dir_listing(cwd, line):
    size, name = line.split(" ")
    if size == "dir":
        if name not in cwd.children:
            cwd.children[name] = Directory(name=name, parent=cwd)
    else:
        if name not in cwd.children:
            cwd.children[name] = File(name=name, size=int(size), parent=cwd)


def parse_file_structure():
    with open(data_path, "r") as f:
        cwd = None
        root = None
        for line in f:
            line = line.strip()
            if line.startswith("$ "):
                if line[2:5] == "cd ":
                    cwd = get_new_cwd(cwd, line[5:])
                    if cwd.name == "":
                        root = cwd
                else:
                    assert line[2:5] == "ls"
            else:
                # must be output from "ls"
                parse_dir_listing(cwd, line)

    root.compute_sizes()
    return root


file_system_root = parse_file_structure()
# print(json.dumps(file_system_root.to_dict(), indent=2))

# part 1
print(f"Part 1 solution: {file_system_root.sum_small_dirs(100000)}")

# part 2
TOTAL_SPACE = 70000000
FREE_SPACE_REQUIRED = 30000000

space_to_free = FREE_SPACE_REQUIRED - (TOTAL_SPACE - file_system_root.size)

smallest_size = file_system_root.size
for directory in file_system_root.iter_subdirs():
    if directory.size > space_to_free:
        smallest_size = min(smallest_size, directory.size)

print(f"Part 2 solution: {smallest_size}")
