"""Day 7: https://adventofcode.com/2022/day/7"""


def load_input(filepath: str) -> list:
    """Reads input and returns it as list[str]"""
    lines = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines


def update_folder_size(filesystem: dict, cwd: tuple, size: int) -> dict:
    """Add size of cwd to itself and all parent folders"""
    for i in range(len(cwd)):
        filesystem[cwd[: i + 1]] += size
    return filesystem


def create_filesystem(logs: list) -> dict:
    """Creates filesystem from logs"""
    filesystem = {("root",): 0}
    cwd = ("root",)
    dirsize = 0
    for line in logs:
        if line.startswith("$ ls"):
            continue
        if line.startswith("dir"):
            dirname = line.split(" ")[-1]
            filesystem[cwd + (dirname,)] = 0
            continue
        if line.startswith("$ cd"):
            filesystem = update_folder_size(filesystem, cwd=cwd, size=dirsize)
            dirsize = 0
            change_to = line.split(" ")[-1]
            if change_to == "/":
                cwd = ("root",)
            elif change_to == "..":
                cwd = cwd[:-1]
            else:
                cwd = cwd + (change_to,)
            continue
        # Line that represents file
        size, _ = line.split(" ")
        dirsize += int(size)
    # Update filesystem with the last information
    filesystem = update_folder_size(filesystem=filesystem, cwd=cwd, size=dirsize)
    return filesystem


def part_one(filesystem: dict) -> int:
    """Calculates total size of directories with size under 100000"""
    total_size = 0
    for size in filesystem.values():
        if size > 100_000:
            continue
        total_size += size
    return total_size


def part_two(filesystem: dict) -> int:
    """Returns total size of directory to be deleted"""
    disk_space = 70000000
    min_free_space = 30000000
    unused_space = disk_space - filesystem[("root",)]
    if unused_space > min_free_space:
        return 0
    space_to_free = min_free_space - unused_space
    candidates = [size for size in filesystem.values() if size >= space_to_free]
    return min(candidates)


if __name__ == "__main__":
    terminal_logs = load_input("input")
    fs = create_filesystem(terminal_logs)
    print(f"Part one: Total size of folders under 100000: {part_one(fs)}")
    print(f"Part two: Size of the folder to be deleted: {part_two(fs)}")
