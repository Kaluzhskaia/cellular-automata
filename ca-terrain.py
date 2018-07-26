# -*- coding: utf-8 -*-

"""Simple creation of a smooth, random landscape by using a cellular automaton. The code is implemented in Python
and matplotlib. Initially, a random distribution of land and water tiles spawns. A CA then decides which cells turn
into water and which into land. This creates a smooth landscape with only land and water tiles. In the final step,
a heat diffusion algorithm averages over all tiles and blurs the boundaries between land and water to create beaches. Tiles can be made land by clicking and the animation can be controlled by the keyboard (spacebar to play/pause append the right arrow button to advance by one frame). The final result is a bit similar to a Perlin noise terrain."""

# first we import necessary packages: numpy (for arrays), pyplot and animation (for visualization)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# then we declare necessary global variables
rows = 100       # number of rows
cols = 100       # number of columns
land = 1.0       # value of a cell that is land
water = 0.0      # value of a water cell
pause = True     # pause flag
created = False  # flag for finishing formation
smoothing_steps = 2
counter = 0

# we create a random distribution of water and land tiles
cell = np.random.choice([land, water], size=(rows, cols))

# we need a function that updates the plot each frame
def update(*args):
    global counter
    if not pause and not created:
        advance()
    elif not pause and created and counter < smoothing_steps:
        smooth()
        counter += 1

# this is the main function that advances the animation by one frame (time step)
def advance(*args):
    global created
    global cell
    # we create a new (actual) copy of all cell states
    newcell = cell.copy()
    # and then sum up the values of all neighboring cells
    for i in range(rows):
        for j in range(cols):
            total = (cell[i, (j - 1) % cols] + cell[i, (j + 1) % cols] + cell[(i - 1) % rows, j] + cell[(i + 1) % rows, j] + cell[(i - 1) % rows, (j - 1) % cols] + cell[(i - 1) % rows, (j + 1) % cols] + cell[(i + 1) % rows, (j - 1) % cols] + cell[(i + 1) % rows, (j + 1) % cols])
            # now comes the decision, if the cell should live in the next time step
            if cell[i, j] == land:
                if total < 4:
                    newcell[i, j] = water
            else:
                if total >= 5:
                    newcell[i, j] = land
    if (newcell == cell).all():
        created = True
        print "Formation stopped."
    # the new cells are now the old cells and are returned
    grid.set_data(newcell)
    cell = newcell
    return [grid]

# now we smooth out the boundaries
def smooth(*args):
    global cell
    erosion = cell.copy()
    for i in range(rows):
        for j in range(cols):
            total = (cell[i, j] + cell[i, (j - 1) % cols] + cell[i, (j + 1) % cols] + cell[(i - 1) % rows, j] + cell[(i + 1) % rows, j] + cell[(i - 1) % rows, (j - 1) % cols] + cell[(i - 1) % rows, (j + 1) % cols] + cell[(i + 1) % rows, (j - 1) % cols] + cell[(i + 1) % rows, (j + 1) % cols])
            avg = np.sqrt(total/9.0)
            erosion[i, j] = avg
    grid.set_data(erosion)
    cell = erosion
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
            cell[i, j] = 1.0
            grid.set_data(cell)
    return grid

# plot and animation commands
fig = plt.figure(figsize=(8, 5))
ax = plt.subplot()
grid = ax.matshow(cell, cmap="terrain_r")
fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('button_press_event', click)
fig.colorbar(grid)
ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
