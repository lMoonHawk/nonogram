import tkinter as tk
from config import *


def mark(puzzle: tk.Canvas, event: tk.Event, clue_boxes, click_type: int, held: bool = False):
    """Mark the cell being clicked on, or hovered over.

    Args:
        puzzle (tk.Canvas): main canvas containing the cells
        event (tk.Event): event triggered on mouse button
        click_type (int): 1 indicates a left click, -1 indicates a right click
        held (bool, optional): Indicates if the event has been triggered while holding the mouse button down. Defaults to False.
    """
    global override, click_coord, click_direction

    # If the mouse button is held, snap to the line
    if held and max(abs(click_coord[0] - event.x), abs(click_coord[1] - event.y)) > cell_size:
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
        puzzle.itemconfig(cell, stipple="@cross.xbm", fill="#c8c8c8", offset="nw")
        grid[row][col] = -1
    if not held:
        click_coord = event.x, event.y
        click_direction = None

    gui_matching(row, col, clue_boxes, puzzle)


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

    fill_tags = []
    if fill:
        fill_tags.append(canvas.create_arc(x2 - 2 * rad, y1, x2, y1 + 2 * rad, fill=fill, outline=fill))
        fill_tags.append(canvas.create_arc(x2 - 2 * rad, y2 - 2 * rad, x2, y2, start=3 * 90, fill=fill, outline=fill))
        fill_tags.append(canvas.create_arc(x1, y2 - 2 * rad, x1 + 2 * rad, y2, start=2 * 90, fill=fill, outline=fill))
        fill_tags.append(canvas.create_arc(x1, y1, x1 + 2 * rad, y1 + 2 * rad, start=1 * 90, fill=fill, outline=fill))
        fill_tags.append(canvas.create_rectangle(x1 + rad, y1, x2 - rad, y2, fill=fill, width=0))
        fill_tags.append(canvas.create_rectangle(x1, y1 + rad, x2, y2 - rad, fill=fill, width=0))

    if width:
        canvas.create_line(x1 + rad, y1, x2 - rad, y1, fill=outline, width=width)
        canvas.create_line(x1 + rad, y2, x2 - rad, y2, fill=outline, width=width)
        canvas.create_line(x1, y1 + rad, x1, y2 - rad, fill=outline, width=width)
        canvas.create_line(x2, y1 + rad, x2, y2 - rad, fill=outline, width=width)
        canvas.create_arc(x2 - 2 * rad, y1, x2, y1 + 2 * rad, start=0 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x2 - 2 * rad, y2 - 2 * rad, x2, y2, start=3 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x1, y2 - 2 * rad, x1 + 2 * rad, y2, start=2 * 90, style="arc", outline=outline, width=width)
        canvas.create_arc(x1, y1, x1 + 2 * rad, y1 + 2 * rad, start=1 * 90, style="arc", outline=outline, width=width)

    return fill_tags


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


def gui_matching(row, col, clue_boxes, puzzle):
    [
        [horizontal_clues, horizontal_boxes, horizontal_clues_tags],
        [vertical_clues, vertical_boxes, vertical_clues_tags],
    ] = clue_boxes

    line_row = grid[row]
    line_col = [grid[k][col] for k in range(len(grid))]

    matched_idx_row = matching(clues[1][row], line_row)
    matched_idx_col = matching(clues[0][col], line_col)

    # Columns
    for j, _ in enumerate(clues[0][col]):
        fill = "black"
        if j in matched_idx_col:
            fill = "grey"
        vertical_clues.itemconfig(vertical_clues_tags[col][j], fill=fill)

    fill = "#bbd0f2"
    if len(matched_idx_col) == len(clues[0][col]):
        fill = "#ebf1fa"
        for i in range(nrow):
            if grid[i][col] != 1:
                grid[i][col] = -1
                cell = (i * ncol + col + 1,)
                puzzle.itemconfig(cell, stipple="@cross.xbm", fill="#c8c8c8", offset="nw")

    # Fill all shapes making up the rounded rectangle
    for shape in vertical_boxes[col]:
        vertical_clues.itemconfig(shape, fill=fill, outline=fill)

    # Rows
    for i, _ in enumerate(clues[1][row]):
        fill = "black"
        if i in matched_idx_row:
            fill = "grey"
        horizontal_clues.itemconfig(horizontal_clues_tags[row][i], fill=fill)

    fill = "#bbd0f2"
    if len(matched_idx_row) == len(clues[1][row]):
        fill = "#ebf1fa"
        for j in range(ncol):
            if grid[row][j] != 1:
                grid[row][j] = -1
                cell = (row * ncol + j + 1,)
                puzzle.itemconfig(cell, stipple="@cross.xbm", fill="#c8c8c8", offset="nw")
    # Fill all shapes making up the rounded rectangle
    for shape in horizontal_boxes[row]:
        horizontal_clues.itemconfig(shape, fill=fill, outline=fill)
