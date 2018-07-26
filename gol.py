# -*- coding: utf-8 -*-

"""This is a simple implementation of Conway's Game of Life in Python. It uses matplotlib's matshow to represent the cells. Cells can be flipped by clicking and the animation can be controlled by the keyboard (spacebar to play/pause append the right arrow button to advance by one frame)."""

# first we import necessary packages: numpy (for arrays), pyplot and animation (for visualization)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# then we declare necessary global variables
rows = 50       # number of rows
cols = 100      # number of columns
alive = 1       # value of a cell that is alive
dead = 0        # value of a dead cell
pause = True    # pause flag

# now we can create the grid and fill them with dead cells
cell = np.full((rows, cols), dead)
# we add an interesting starting configuration (R-pentomino)
cell[4, 4] = cell[3, 4] = cell[5, 4] = cell[3, 5] = cell[4, 3] = alive

# we need a function that updates the plot each frame
def update(*args):
    if not pause:
        advance()

# this is the main function that advances the animation by one frame (time step)
def advance(*args):
    global cell
    # we create a new (actual) copy of all cell states
    newcell = cell.copy()
    # and then sum up the values of all neighboring cells
    for i in range(rows):
        for j in range(cols):
            total = (cell[i, (j - 1) % cols] + cell[i, (j + 1) % cols] + cell[(i - 1) % rows, j] + cell[(i + 1) % rows, j] + cell[(i - 1) % rows, (j - 1) % cols] + cell[(i - 1) % rows, (j + 1) % cols] + cell[(i + 1) % rows, (j - 1) % cols] + cell[(i + 1) % rows, (j + 1) % cols])
            # now comes the decision, if the cell should live in the next time step
            if cell[i, j] == alive:
                if (total < 2) or (total > 3):
                    newcell[i, j] = dead
            else:
                if total == 3:
                    newcell[i, j] = alive
    # the new cells are now the old cells and are returned
    grid.set_data(newcell)
    cell = newcell
    return [grid]

# this catches keyboard events (spacebar for play/pause, right arrow key for advancing one frame)
def press(event):
    global pause
    if event.key == " ":
        pause = not pause
        return pause
    elif event.key == "right":
        advance()

# catches mouseclick events for flipping states of cells
def click(event):
    if pause:
        global cell
        if isinstance(event.xdata, float) and isinstance(event.ydata, float):
            j = int(round(event.xdata))
            i = int(round(event.ydata))
            cell[i, j] = not cell[i, j]
            grid.set_data(cell)
    return grid

# plot and animation commands
fig = plt.figure(figsize=(8, 5))
ax = plt.subplot()
grid = ax.matshow(cell, cmap="Greys")
fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('button_press_event', click)
ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
