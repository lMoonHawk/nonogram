def matching(clue: list[int], line: list[int], complete: bool = True) -> list[int]:
    """Perform three checks on the line for clue matching.\n
    *First, check if the line contains all the blocks in the clue.\n
    *If false, check if some block clues are identifiable from each side of the line.

    Args:
        clue (list[int]): Clue listing the blocks with which to match the line.
        line (list[int]): Status of each cell in the line (0:unmarked, 1: filled, -1:crossed)
        complete (bool, optional): Complete or partial match. Defaults to True.

    Returns:
        list[int]: indexes of the clue blocks that are represented on the line
    """
    stack = line[:]
    # blocks lists the size of blocks separated by crossed or unmarked cells
    blocks = [0]
    while stack:
        el = stack.pop(0)
        if el == 1:
            blocks[-1] += 1
        else:
            blocks.append(0)
            # If we are in a partial matching mode, an unmarked cell stops the process
            if not complete and el == 0:
                break
    # We remove the separators to only keep the size of blocks on the line
    blocks = [el for el in blocks if el > 0]

    # This function is first called on a complete matching mode.
    # If all blocks are found, return all indexes
    # If not, try a partial match on each side of the line
    if complete:
        if blocks == clue:
            return list(range(len(clue)))
        else:
            x = matching(clue, line, complete=False)
            y = matching(clue[::-1], line[::-1], complete=False)
            # Reverse the indexes as both line and clue were inverted to check the other side
            y = [len(clue) - 1 - el for el in y]
            return x.union(y)
    # We are in a partial matching mode
    # Match the blocks in the clue to the blocks on the line one by one getting the indexes
    else:
        out = set()
        for i, (clue_block, line_block) in enumerate(zip(clue, blocks)):
            if clue_block == line_block:
                out.add(i)
            else:
                break
        return out


clue = [10, 3, 3]
line = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0, 2] expected")

clue = [10, 3, 3]
line = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [2] expected")

clue = [10, 3, 3]
line = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0, 1, 2] expected")

clue = [4, 5, 2]
line = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [] expected")

clue = [4, 5, 2]
line = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0] expected")

clue = [4, 5, 2]
line = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0, 2] expected")

clue = [6]
line = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(f"{list(matching(clue, line))} / [0] expected")

clue = [6]
line = [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(f"{list(matching(clue, line))} / [] expected")

clue = [4, 5, 2]
line = [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]
print(f"{list(matching(clue, line))} / [] expected")

clue = [4, 5, 2]
line = [-1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0]
print(f"{list(matching(clue, line))} / [0] expected")

clue = [4, 5]
line = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(f"{list(matching(clue, line))} / [0, 1] expected")

clue = [2]
line = [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
print(f"{list(matching(clue, line))} / [] expected")
