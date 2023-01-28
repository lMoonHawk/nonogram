import json
from copy import deepcopy

puzzle = "1"

# Visualization:
# filled:  ■ (alt 254)
# crossed: x (x) × (alt 0215) · (alt 0183) · (alt 250)
visualization = {-1: "·", 0: " ", 1: "■"}

digit_visu = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "a",
    "11": "b",
    "12": "c",
    "13": "d",
    "14": "e",
    "15": "f",
    "16": "g",
    "17": "h",
    "18": "i",
    "19": "j",
    "20": "k",
}


def show():
    max_size_col = max([len(clue) for clue in clues[0]])
    max_size_row = max([len(clue) for clue in clues[1]])

    # print column clues
    for row in range(max_size_col):
        print(" " * (max_size_row * 2), end="")
        for clue in clues[0]:
            padding = max_size_col - len(clue)
            out = padding * [" "] + [str(digit) for digit in clue]
            out = digit_visu[out[row]] if out[row] != " " else out[row]
            print(out, end=" ")
        print()

    for i, row in enumerate(grid):
        if i % 5 == 0:
            print(" " * (max_size_row * 2 - 1) + "—" * (ncol * 2 + 1))
        # Show clues
        padding = max_size_row - len(clues[1][i])
        out = padding * "  " + " ".join([digit_visu[str(clue)] for clue in clues[1][i]])
        print(out, end="")

        for j, cell in enumerate(row):
            if j % 5 == 0:
                print("|", end="")
            else:
                print(" ", end="")
            print(visualization[cell], end="")
        print("|")
    print(" " * (max_size_row * 2 - 1) + "—" * (ncol * 2 + 1))


def blank_combin(n, k, n_ini=None):
    if not n_ini:
        n_ini = n
    if n == 1:
        return [[k]]
    ways = []
    for i in range(k + 1):
        if i == 0 and (0 < n < n_ini):
            continue
        sub_ways = blank_combin(n - 1, k - i, n_ini)
        for sub_way in sub_ways:
            ways.append([i] + sub_way)
    return ways


def fill_cells(cells, col_row, index):
    for i, cell in enumerate(cells):
        # We are looking at columns
        if col_row == 0:
            row, col = i, index
        else:
            row, col = index, i

        if cell:
            grid[row][col] = cell


with open(f"puzzles/puzzle{puzzle}.json") as file:
    clues = file.read()

clues = json.loads(clues)

ncol = len(clues[0])
nrow = len(clues[1])

grid = [[0] * ncol for _ in range(nrow)]


def common(col_row):

    for i, clue in enumerate(clues[col_row]):
        # We are looking at columns
        if col_row == 0:
            ncells = nrow
            line = [grid[j][i] for j in range(nrow)]
        else:
            ncells = ncol
            line = grid[i]

        # If row/col empty, check to see if it is possible to fill some cells
        if all([1 if not cell else 0 for cell in line]):
            remainder = ncells - (sum(clue) + len(clue) - 1)
            if max(clue) <= remainder:
                continue

        k = ncells - sum(clue)
        n = len(clue) + 1

        mask = None
        for possibility in blank_combin(n, k):
            # Value = possible combination for the clue
            value = [-1] * possibility[0]
            for sep, digit in zip(possibility[1:], clue):
                value += [1] * digit
                value += [-1] * sep

            # The constraint is what cells are already filled/crossed in that line
            # If the combination does not respect the current line, continue
            constraint = [not (x != 0 and y != x) for x, y in zip(line, value)]
            if all(constraint):
                # Iteratively mark/unmark cells
                # Mask keeps track of the common states of cells in that line
                if not mask:
                    mask = value
                else:
                    mask = [x * (x == y) for x, y in zip(value, mask)]

        fill_cells(mask, col_row, i)


def solve():
    done = False
    while not done:
        input()
        show()
        grid_check = deepcopy(grid)
        common(0)
        common(1)

        if grid == grid_check:
            done = True


solve()
