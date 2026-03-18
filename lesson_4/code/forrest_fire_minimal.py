import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


area = 160
iterations = 500
p_ignition = 0.00002
p_planting = 0.004
grid = np.zeros((area, area), dtype=int)

colors = ListedColormap(np.array([
    [76, 66, 70],
    [118, 176, 65],
    [228, 87, 46],
]) / 255)


def detect_fire(row: int, col: int, grid: np.ndarray) -> bool:
    width, height = grid.shape
    neighborhood = grid[max(0, row - 1):min(width, row + 2), max(0, col - 1):min(height, col + 2)]
    return np.max(neighborhood) == 2


def update_cell_state(cell_state: int, fire_in_neighborhood: bool, p_planting: float, p_ignition: float) -> int:
    if cell_state == 0:
        return int(np.random.random() < p_planting)
    if cell_state == 1:
        random_ignition = np.random.random() < p_ignition
        return 2 if fire_in_neighborhood or random_ignition else 1
    return 0


for _ in range(iterations):
    new_grid = np.zeros((area, area), dtype=int)
    for row in range(area):
        for col in range(area):
            fire_in_neighborhood = detect_fire(row, col, grid)
            new_grid[row, col] = update_cell_state(int(grid[row, col]), fire_in_neighborhood, p_planting, p_ignition)
    grid = new_grid
    plt.figure(1)
    plt.clf()
    plt.imshow(grid, cmap=colors, vmin=0, vmax=2)
    plt.pause(0.001)

plt.show()
