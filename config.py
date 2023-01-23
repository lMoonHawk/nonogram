block_size = 150
cell_size = block_size // 5
puzzle_nr = 1
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
