import tkinter as tk
from config import *
from gui_functions import mark


root = tk.Tk()
root.title("Nonogram Solver")
icon = tk.PhotoImage(file="icon.png")
root.iconphoto(False, icon)

# Create the puzzle
puzzle = tk.Canvas(root, bg="white", width=block_size * ncol // 5, height=block_size * nrow // 5)
puzzle.pack()

# Add the cells
for i in range(nrow):
    for j in range(ncol):
        k = cell_size
        puzzle.create_rectangle(j * k, i * k, (j + 1) * k, (i + 1) * k, outline="#AAAAAA", fill="white")

# Add the blocks
for i in range(nrow // 5):
    row = []
    for j in range(ncol // 5):
        k = block_size
        big_rect = puzzle.create_rectangle(i * k, j * k, (i + 1) * k, (j + 1) * k, width=2, outline="#555555")

# Bind mouse buttons to marking the cells
puzzle.bind("<Button-1>", lambda event: mark(puzzle, event, 1))
puzzle.bind("<B1-Motion>", lambda event: mark(puzzle, event, 1, held=True))
puzzle.bind("<Button-3>", lambda event: mark(puzzle, event, -1))
puzzle.bind("<B3-Motion>", lambda event: mark(puzzle, event, -1, held=True))

root.mainloop()
