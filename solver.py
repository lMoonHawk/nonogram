import tkinter as tk
from config import *
from gui_functions import mark
import json


root = tk.Tk()
root.title("Nonogram Solver")
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

with open(f"puzzles/puzzle{puzzle_nr}.json") as file:
    clues = file.read()

clues = json.loads(clues)

clues_row_frame = tk.Frame(master=root)
for col, clue in enumerate(clues[0]):
    clue_text = "\n".join([str(block) for block in clue])
    frame = tk.Frame(
        master=clues_row_frame,
        height=20 * 4,
        highlightbackground="#697278",
        highlightthickness=1,
        width=cell_size,
        bg="#e3f2fa",
    )
    frame.pack_propagate(False)
    label = tk.Label(
        frame,
        text=clue_text,
        bg="#e3f2fa",
        font=("Segoe UI", "10", "bold"),
    )

    label.pack(side="bottom")
    frame.pack(side="left")

clues_row_frame.grid(row=0, column=1)

clues_col_frame = tk.Frame(root)
for row, clue in enumerate(clues[1]):
    clue_text = "  ".join([str(block) for block in clue])
    frame = tk.Frame(
        master=clues_col_frame,
        height=cell_size,
        highlightbackground="#697278",
        highlightthickness=1,
        width=20 * 5,
        bg="#e3f2fa",
    )
    frame.pack_propagate(False)
    label = tk.Label(
        frame,
        text=clue_text,
        bg="#e3f2fa",
        font=("Segoe UI", "10", "bold"),
    )
    label.pack(side="right")
    frame.pack(side="bottom")

clues_col_frame.grid(row=1, column=0)

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

root.mainloop()
