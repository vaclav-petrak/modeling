import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


forest_color_map = np.array([
    [76, 66, 70],
    [118, 176, 65],
    [228, 87, 46],
]) / 255

forest = np.array([
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 2, 1, 0],
    [1, 1, 2, 0, 0],
    [1, 0, 0, 0, 0],
])

plt.imshow(forest, cmap=ListedColormap(forest_color_map), vmin=0, vmax=2)
plt.axis("off")
plt.show()
