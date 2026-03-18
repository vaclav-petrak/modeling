import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def detect_fire(row: int, col: int, grid: np.ndarray) -> bool:
    width, height = grid.shape
    neighborhood = grid[max(0, row - 1):min(width, row + 2), max(0, col - 1):min(height, col + 2)]
    return np.max(neighborhood) == 2


def update_cell_state(cell_state: int, fire_in_neighborhood: bool, planting_chance: float, ignition_chance: float) -> int:
    if cell_state == 0:
        return int(np.random.random() < planting_chance)
    if cell_state == 1:
        random_ignition = np.random.random() < ignition_chance
        return 2 if fire_in_neighborhood or random_ignition else 1
    return 0


area = 160
iterations = 1000
initial_coverage = 0.2
ignition_chance = 0.00002
planting_chance = 0.0040

ground = np.array([76, 66, 70]) / 255
trees = np.array([118, 176, 65]) / 255
fire = np.array([228, 87, 46]) / 255
cmap = ListedColormap([ground, trees, fire])

grid = (np.random.random((area, area)) < initial_coverage).astype(int)
tree_count = np.full(iterations, np.nan)
fire_count = np.full(iterations, np.nan)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
for i in range(iterations):
    new_grid = np.zeros((area, area), dtype=int)
    for row in range(area):
        for col in range(area):
            fire_in_neighborhood = detect_fire(row, col, grid)
            new_grid[row, col] = update_cell_state(int(grid[row, col]), fire_in_neighborhood, planting_chance, ignition_chance)
    grid = new_grid
    tree_count[i] = np.sum(grid == 1)
    fire_count[i] = np.sum(grid == 2)

    ax1.clear()
    ax1.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    ax1.axis("off")
    ax1.set_aspect("equal")

    ax2.clear()
    ax2.plot(tree_count, linewidth=2, color=trees)
    ax2.plot(fire_count * 10, linewidth=2, color=fire)
    ax2.set_ylim(0, 12000)
    ax2.set_xlim(0, iterations)
    ax2.set_ylabel("Tree count")
    ax2.set_xlabel("Time")
    ax2.set_title("Forrest fire simulation")
    plt.pause(0.001)

plt.show()
