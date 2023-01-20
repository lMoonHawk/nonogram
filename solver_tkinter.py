import tkinter as tk
import json
from copy import deepcopy

root = tk.Tk()

block_size = 150
cell_size = block_size // 5

nrow = 20
ncol = 20

grid = [[0] * ncol for _ in range(nrow)]

# Current mode of filling, when the mouse button is held down
# -1: update only crossed cells, 0: empty, 1: filled
# This value depends on the initial clicked cell before the motion
override = 0


def left_click(event):
    global override

    # print(f"clicked at {(event.x, event.y)} ({override=})")
    cell = puzzle.find_closest(event.x, event.y)

    # Only fill if the item is a cell (+2 for border)
    x0, _, x1, _ = puzzle.bbox(cell)
    if x1 - x0 == cell_size + 2:
        row, col = divmod(cell[0], ncol)
        state = grid[row][col]

        if state in [0, -1]:
            puzzle.itemconfig(cell, fill="black", stipple="")
            grid[row][col] = 1

        elif state == 1:
            puzzle.itemconfig(cell, fill="white", stipple="")
            grid[row][col] = 0

        # Only modify same type cells if button held
        override = state


def held_left_click(event):
    global overrides

    # print(f"clicked at {(event.x, event.y)} ({override=})")
    cell = puzzle.find_closest(event.x, event.y)

    # Only fill if the item is a cell (+2 for border)
    x0, _, x1, _ = puzzle.bbox(cell)
    if x1 - x0 == cell_size + 2:
        row, col = divmod(cell[0], ncol)
        state = grid[row][col]

        if override == state and state in [0, -1]:
            puzzle.itemconfig(cell, fill="black", stipple="")
            grid[row][col] = 1

        elif override == state and state == 1:
            puzzle.itemconfig(cell, fill="white", stipple="")
            grid[row][col] = 0


def right_click(event):
    global override

    # print(f"clicked at {(event.x, event.y)} ({override=})")
    cell = puzzle.find_closest(event.x, event.y)

    # Only fill if the item is a cell (+2 for border)
    x0, y0, x1, _ = puzzle.bbox(cell)
    if x1 - x0 == cell_size + 2:
        row, col = divmod(cell[0], ncol)
        state = grid[row][col]

        if state in [1, 0]:
            puzzle.itemconfig(cell, stipple="gray50", fill="#AAAAAA")
            grid[row][col] = -1

        elif state == -1:
            puzzle.itemconfig(cell, fill="white", stipple="")
            grid[row][col] = 0

        # Only modify same type cells if button held
        override = state


def held_right_click(event):
    global override

    # print(f"clicked at {(event.x, event.y)} ({override=})")
    cell = puzzle.find_closest(event.x, event.y)

    # Only fill if the item is a cell (+2 for border)
    x0, y0, x1, _ = puzzle.bbox(cell)
    if x1 - x0 == cell_size + 2:
        row, col = divmod(cell[0], ncol)
        state = grid[row][col]

        if override == state and state in [1, 0]:
            puzzle.itemconfig(cell, stipple="gray50", fill="#AAAAAA")
            grid[row][col] = -1

        elif override == state and state == -1:
            puzzle.itemconfig(cell, fill="white", stipple="")
            grid[row][col] = 0


# Create the puzzle
puzzle = tk.Canvas(root, bg="white", width=block_size * ncol // 5, height=block_size * nrow // 5)
puzzle.pack()

# Add the blocks


for i in range(nrow):
    for j in range(ncol):
        puzzle.create_rectangle(
            j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, outline="#AAAAAA", fill="white"
        )

blocks = []
for i in range(nrow // 5):
    row = []
    for j in range(ncol // 5):
        big_rect = puzzle.create_rectangle(
            i * block_size, j * block_size, (i + 1) * block_size, (j + 1) * block_size, width=2, outline="#555555"
        )
        row.append(big_rect)
    blocks.append(row)

# puzzle.bind("<Motion>", detect_override)
puzzle.bind("<Button-1>", left_click)
puzzle.bind("<B1-Motion>", held_left_click)
puzzle.bind("<Button-3>", right_click)
puzzle.bind("<B3-Motion>", held_right_click)

root.mainloop()
