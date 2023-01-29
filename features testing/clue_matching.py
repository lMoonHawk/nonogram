def matching(clue: list[int], line: list[int], complete=True, rev=False) -> list[int]:
    """Perform three checks on line to clue matching. First, check if the line contains all blocks in the clue.
    If false, check if some block clues are identifiable from each side of the line.

    Args:
        clue (list[int]): Clue listing the blocks with which to match the line.
        line (list[int]): Status of each cell in the line (0:unmarked, 1: filled, -1:crossed)
        complete (bool, optional): Check if all blocks in the clue are present. Defaults to True.
        rev (bool, optional): Check from the other side of the line. Defaults to False.

    Returns:
        list[int]: indexes of blocks matched with the clue
    """
    n = len(clue)
    out = set()

    line_check = line
    if rev:
        line_check = line[::-1]

    count = 0
    block_index = 0
    for k, cell in enumerate(line_check):
        # block is the block in the clue that we are trying to match with
        index = block_index if not rev else n - 1 - block_index
        block = clue[index]

        if cell == 1:
            count += 1
        # We are stopping the streak of filled cells (-1,0 or reached the end)
        if cell in [-1, 0] or k == len(line) - 1:
            # If this streak corresponds to the block, there is a match
            if count == block:
                # Add index to the output
                out.add(index)
                count = 0
                # Try matching next block
                block_index += 1
        # If we are looking for a complete match, ignore 0 and move to next streak
        # If not and we reach a 0, matching stops for this side of the line
        if not complete and cell == 0:
            break

    # We tried one side of the line, try the reverse and add the result
    if not complete and not rev:
        return list(out.union(matching(clue, line, complete=False, rev=True)))
    # We tried to match the whole clue and failed, move on to look at individual blocks matching
    if complete and len(out) != n:
        return list(matching(clue, line, complete=False))

    return out


clue = [10, 3, 3]
line = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0,2] expected")

clue = [10, 3, 3]
line = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [2] expected")

clue = [10, 3, 3]
line = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0,1,2] expected")

clue = [4, 5, 2]
line = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [] expected")

clue = [4, 5, 2]
line = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0] expected")

clue = [4, 5, 2]
line = [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, -1, 1, 1, -1]
print(f"{list(matching(clue, line))} / [0,2] expected")
