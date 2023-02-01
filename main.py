import tkinter as tk
from config import *
from gui_functions import mark, create_rounded_rectangle


root = tk.Tk()
root.title("Nonogram Solver")
icon = tk.PhotoImage(file="img/icon.png")
root.iconphoto(False, icon)

vertical_clues = tk.Canvas(root, width=ncol * cell_size, height=20 * 4)
vertical_clues.grid(row=0, column=1)
horizontal_clues = tk.Canvas(root, width=20 * 5, height=nrow * cell_size)
horizontal_clues.grid(row=1, column=0)

vertical_clues_tags = []
vertical_boxes = []
for i, clue in enumerate(clues[0]):
    tags = create_rounded_rectangle(
        vertical_clues,
        i * cell_size + pad,
        pad,
        (i + 1) * cell_size - pad,
        20 * 4 - pad,
        fill="#bbd0f2",
        rad=7,
        width=1,
    )
    vertical_boxes.append(tags)
    clue_len = len(clue)
    clue_tag = []
    for j, block in enumerate(clue):
        # Block clues have to be individually placed as the fg needs to update when a block is resolved
        tag = vertical_clues.create_text(
            i * cell_size + cell_size // 2,
            20 * 4 - pad - 5 - (clue_len - j - 1) * (font_height),
            text=str(block),
            anchor="s",
            justify="center",
            font=clue_font,
        )
        clue_tag.append(tag)
    vertical_clues_tags.append(clue_tag)

horizontal_clues_tags = []
horizontal_boxes = []
for j, clue in enumerate(clues[1]):
    tags = create_rounded_rectangle(
        horizontal_clues,
        pad,
        j * cell_size + pad,
        20 * 5 - pad,
        (j + 1) * cell_size - pad,
        fill="#bbd0f2",
        rad=7,
    )
    horizontal_boxes.append(tags)
    clue_len = len(clue)
    char_len = 0
    clue_tag = []
    for i, block in enumerate(clue[::-1]):
        tag = horizontal_clues.create_text(
            20 * 5 - pad - 5 - char_len,
            j * cell_size + cell_size // 2,
            text=str(block),
            anchor="e",
            font=clue_font,
        )
        char_len += font_width[len(str(block))] + 2
        clue_tag.append(tag)
    clue_tag.reverse()
    horizontal_clues_tags.append(clue_tag)


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


clue_boxes = [
    [horizontal_clues, horizontal_boxes, horizontal_clues_tags],
    [vertical_clues, vertical_boxes, vertical_clues_tags],
]

# Bind mouse buttons to marking the cells
puzzle.bind("<Button-1>", lambda event: mark(puzzle, event, clue_boxes, 1))
puzzle.bind("<B1-Motion>", lambda event: mark(puzzle, event, clue_boxes, 1, held=True))
puzzle.bind("<Button-3>", lambda event: mark(puzzle, event, clue_boxes, -1))
puzzle.bind("<B3-Motion>", lambda event: mark(puzzle, event, clue_boxes, -1, held=True))

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
