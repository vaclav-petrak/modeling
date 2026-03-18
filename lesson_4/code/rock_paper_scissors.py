import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


size = 200
grid = np.random.randint(1, 4, size=(size, size))
newgrid = grid.copy()

for _ in range(300):
    for r in range(1, size - 1):
        for c in range(1, size - 1):
            neighbourhood = grid[r - 1:r + 2, c - 1:c + 2]
            if grid[r, c] == 1:
                if np.sum(neighbourhood == 2) > 2:
                    newgrid[r, c] = 2
            elif grid[r, c] == 2:
                if np.sum(neighbourhood == 3) > 2:
                    newgrid[r, c] = 3
            else:
                if np.sum(neighbourhood == 1) > 2:
                    newgrid[r, c] = 1
    grid = newgrid.copy()
    plt.figure(1)
    plt.clf()
    plt.imshow(grid, cmap=ListedColormap([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), vmin=1, vmax=3)
    plt.axis("square")
    plt.pause(0.01)

plt.show()
