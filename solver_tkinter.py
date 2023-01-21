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
# Click position, used to keep track of direction when holding the button
click_coord = None
# Line direction when the button is held down
click_direction = None


def mark(cell, click_type, held=False) -> bool:
    """Mark the cell being clicked on, or hovered over.

    Args:
        cell (_type_): tag of the cell clicked or hovered over
        click_type (int): 1 indicates a left click, -1 indicates a right click
        held (bool, optional): Indicates if the event has been triggered while holding the mouse button down. Defaults to False.

    Returns:
        bool: True if a cell cell has been marked
    """
    global override

    # Only fill if the item is a small cell (+2 for border)
    x0, _, x1, _ = puzzle.bbox(cell)
    if x1 - x0 != cell_size + 2:
        return False

    # Get row, column and current state of the cell in the grid
    row, col = divmod(cell[0], ncol)
    state = grid[row][col]

    # If button is held, state of the cell hovered must be the same as override
    condition = True
    if held:
        condition = override == state
    # If button is pressed, override becomes the current state
    else:
        override = state

    # Click is of the same time as the cell: erase
    if condition and state == click_type:
        puzzle.itemconfig(cell, fill="white", stipple="")
        grid[row][col] = 0
    # Left click a different cell type
    if click_type == 1 and condition and state in [0, -1]:
        puzzle.itemconfig(cell, fill="black", stipple="")
        grid[row][col] = 1
    # Right click a different cell type
    if click_type == -1 and condition and state in [1, 0]:
        puzzle.itemconfig(cell, stipple="gray50", fill="#AAAAAA")
        grid[row][col] = -1

    return True


def snap_line(event: tk.Event) -> tuple:
    """Keeps track of the direction of the line the user went for.

    Args:
        event (tk.Event): event triggered on mouse button held down

    Returns:
        tuple: Coordinates of the mouse, projected to the line created from the initially clicked cell
    """
    global overrides, click_coord, click_direction
    click_x, click_y = click_coord

    if click_direction is None:
        # User went for a horizontal line
        if abs(event.x - click_x) > abs(event.y - click_y):
            click_direction = 0
        # User went for a vertical line
        else:
            click_direction = 1

    if click_direction == 0:
        x = event.x
        y = click_y
    else:
        x = click_x
        y = event.y

    return x, y


def left_click(event: tk.Event):
    global override, click_coord, click_direction

    cell = puzzle.find_closest(event.x, event.y)

    if mark(cell, 1):
        click_coord = event.x, event.y
        click_direction = None


def held_left_click(event: tk.Event):
    x, y = snap_line(event)
    cell = puzzle.find_closest(x, y)

    mark(cell, 1, held=True)


def right_click(event: tk.Event):
    global override, click_coord, click_direction

    cell = puzzle.find_closest(event.x, event.y)

    if mark(cell, -1):
        click_coord = event.x, event.y
        click_direction = None


def held_right_click(event: tk.Event):
    x, y = snap_line(event)
    cell = puzzle.find_closest(x, y)

    mark(cell, -1, held=True)


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

puzzle.bind("<Button-1>", left_click)
puzzle.bind("<B1-Motion>", held_left_click)
puzzle.bind("<Button-3>", right_click)
puzzle.bind("<B3-Motion>", held_right_click)

root.mainloop()
