import json

block_size = 150
cell_size = block_size // 5
puzzle_nr = 1
nrow = 20
ncol = 20

with open(f"puzzles/puzzle{puzzle_nr}.json") as file:
    clues = file.read()

clues = json.loads(clues)

# Padding between clues
pad = 2
clue_font = ("Segoe UI", 10, "bold")
# Height in pixel for a line of ("Segoe UI", 10, "bold")
font_height = 17
# Width in pixel of 1 and 2 chars of ("Segoe UI", 10, "bold")
font_width = {1: 9, 2: 16}
# test = vertical_clues.create_text(...)
# coord = vertical_clues.bbox(test)
# print(f"height={coord[3]-coord[1]}, width={coord[2]-coord[0]}")


grid = [[0] * ncol for _ in range(nrow)]

# Current mode of filling, when the mouse button is held down
# -1: update only crossed cells, 0: empty, 1: filled
# This value depends on the initial clicked cell before the motion
override = 0
# Click position, used to keep track of direction when holding the button
click_coord = None
# Line direction when the button is held down
click_direction = None
