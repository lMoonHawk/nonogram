import tkinter as tk
from config import *
from gui_functions import mark, create_rounded_rectangle
import json


root = tk.Tk()
root.title("Nonogram Solver")
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

with open(f"puzzles/puzzle{puzzle_nr}.json") as file:
    clues = file.read()

clues = json.loads(clues)

vertical_clues = tk.Canvas(root, width=ncol * cell_size, height=20 * 4)
vertical_clues.grid(row=0, column=1)
horizontal_clues = tk.Canvas(root, width=20 * 5, height=nrow * cell_size)
horizontal_clues.grid(row=1, column=0)

pad = 2
# Height in pixel for a line of ("Segoe UI", 10, "bold")
font_height = 17
# Width in pixel of 1 and 2 chars of ("Segoe UI", 10, "bold")
font_width = {1: 9, 2: 16}
# test = vertical_clues.create_text(...)
# coord = vertical_clues.bbox(test)
# print(f"height={coord[3]-coord[1]}, width={coord[2]-coord[0]}")

for i, clue in enumerate(clues[0]):
    create_rounded_rectangle(
        vertical_clues,
        i * cell_size + pad,
        pad,
        (i + 1) * cell_size - pad,
        20 * 4 - pad,
        fill="#bbd0f2",
        rad=7,
        width=1,
    )
    clue_len = len(clue)
    for j, block in enumerate(clue):
        # Block clues have to be individually placed as the fg needs to update when a block is resolved
        test = vertical_clues.create_text(
            i * cell_size + cell_size // 2,
            20 * 4 - pad - 5 - (clue_len - j - 1) * (font_height),
            text=str(block),
            anchor="s",
            justify="center",
            font=("Segoe UI", 10, "bold"),
        )

for j, clue in enumerate(clues[1]):
    create_rounded_rectangle(
        horizontal_clues,
        pad,
        j * cell_size + pad,
        20 * 5 - pad,
        (j + 1) * cell_size - pad,
        fill="#bbd0f2",
        rad=7,
    )
    clue_len = len(clue)
    char_len = 0
    for i, block in enumerate(clue[::-1]):
        horizontal_clues.create_text(
            20 * 5 - pad - 5 - char_len,
            j * cell_size + cell_size // 2,
            text=str(block),
            anchor="e",
            font=("Segoe UI", 10, "bold"),
        )
        char_len += font_width[len(str(block))] + 2

# Create the puzzle
puzzle = tk.Canvas(root, bg="white", width=block_size * ncol // 5, height=block_size * nrow // 5)
puzzle.grid(row=1, column=1, padx=0, pady=0)

# Add the cells
for i in range(nrow):
    for j in range(ncol):
        k = cell_size
        puzzle.create_rectangle(
            j * k + 1, i * k + 1, (j + 1) * k + 1, (i + 1) * k + 1, outline="#AAAAAA", fill="white"
        )

# Add the blocks
for i in range(nrow // 5):
    row = []
    for j in range(ncol // 5):
        k = block_size
        big_rect = puzzle.create_rectangle(
            i * k + 1, j * k + 1, (i + 1) * k + 1, (j + 1) * k + 1, width=1, outline="#555555"
        )

# Bind mouse buttons to marking the cells
puzzle.bind("<Button-1>", lambda event: mark(puzzle, event, 1))
puzzle.bind("<B1-Motion>", lambda event: mark(puzzle, event, 1, held=True))
puzzle.bind("<Button-3>", lambda event: mark(puzzle, event, -1))
puzzle.bind("<B3-Motion>", lambda event: mark(puzzle, event, -1, held=True))


# Buttons
menu = tk.Frame(root, width=20 * 5 - 5, height=20 * 4 - 5)
menu.pack_propagate(False)
button_new = tk.Button(menu, text="New")
button_save = tk.Button(menu, text="Save")
button_img = tk.Button(menu, text="Load")
button_new.pack(fill="x")
button_save.pack(fill="x")
button_img.pack(fill="x")
menu.grid(row=0, column=0)
root.mainloop()
