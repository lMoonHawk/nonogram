import tkinter as tk
from config import *


def mark(puzzle: tk.Canvas, event: tk.Event, click_type: int, held: bool = False):
    """Mark the cell being clicked on, or hovered over.

    Args:
        puzzle (tk.Canvas): main canvas containing the cells
        event (tk.Event): event triggered on mouse button
        click_type (int): 1 indicates a left click, -1 indicates a right click
        held (bool, optional): Indicates if the event has been triggered while holding the mouse button down. Defaults to False.
    """
    global override, click_coord, click_direction

    # If the mouse button is held, snap to the line
    if held:
        x, y = snap_line(event)
    else:
        x, y = event.x, event.y

    cell = puzzle.find_closest(x, y)

    # Only fill if the item is a small cell (+2 for border)
    x0, _, x1, _ = puzzle.bbox(cell)
    if x1 - x0 != cell_size + 2:
        return

    # Tag layout for a 3x3:
    # 1,2,3
    # 4,5,6
    # 7,8,9
    # subtracting 1 from the tag yields row and column in the grid with div and mod
    row, col = divmod(cell[0] - 1, ncol)
    state = grid[row][col]

    # If button is held, state of the cell hovered must be the same as override
    condition = True
    if held:
        condition = override == state
    # If button is pressed, override becomes the current state
    # Then, if the mouse button is held only change cells of type override (current state)
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
    if not held:
        click_coord = event.x, event.y
        click_direction = None


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


def create_rounded_rectangle(canvas, x1, y1, x2, y2, rad=None, fill=None, outline="black", width=1):

    if rad is None:
        rad = min(x2 - x1, y2 - y1) // 10
    rad = max(min(min(x2 - x1, y2 - y1) // 2, rad), 0)

    if fill:
        canvas.create_arc(x2 - 2 * rad, y1, x2, y1 + 2 * rad, fill=fill, outline=fill)
        canvas.create_arc(x2 - 2 * rad, y2 - 2 * rad, x2, y2, start=3 * 90, fill=fill, outline=fill)
        canvas.create_arc(x1, y2 - 2 * rad, x1 + 2 * rad, y2, start=2 * 90, fill=fill, outline=fill)
        canvas.create_arc(x1, y1, x1 + 2 * rad, y1 + 2 * rad, start=1 * 90, fill=fill, outline=fill)
        canvas.create_rectangle(x1 + rad, y1, x2 - rad, y2, fill=fill, width=0)
        canvas.create_rectangle(x1, y1 + rad, x2, y2 - rad, fill=fill, width=0)

    if width:
        canvas.create_line(x1 + rad, y1, x2 - rad, y1, fill=outline, width=width)
        canvas.create_line(x1 + rad, y2, x2 - rad, y2, fill=outline, width=width)
        canvas.create_line(x1, y1 + rad, x1, y2 - rad, fill=outline, width=width)
        canvas.create_line(x2, y1 + rad, x2, y2 - rad, fill=outline, width=width)
        canvas.create_arc(x2 - 2 * rad, y1, x2, y1 + 2 * rad, start=0 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x2 - 2 * rad, y2 - 2 * rad, x2, y2, start=3 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x1, y2 - 2 * rad, x1 + 2 * rad, y2, start=2 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x1, y1, x1 + 2 * rad, y1 + 2 * rad, start=1 * 90, style="arc", outline=outline, width=width)
