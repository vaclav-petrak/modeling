import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


L = 160
num_steps = 500
f = 0.00002
p = 0.004

EMPTY = 0
TREE = 1
BURNING = 2


def is_neighbor_burning(r: int, c: int, grid: np.ndarray, grid_size: int, burning_state: int) -> bool:
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr = r + dr
            nc = c + dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size and grid[nr, nc] == burning_state:
                return True
    return False


def calculate_next_state(current_state: int, neighbor_is_burning: bool, p_growth: float, f_ignition: float, empty: int, tree: int, burning: int) -> int:
    if current_state == empty:
        return tree if np.random.random() < p_growth else empty
    if current_state == tree:
        random_ignition = np.random.random() < f_ignition
        return burning if neighbor_is_burning or random_ignition else tree
    if current_state == burning:
        return empty
    return current_state


grid = np.zeros((L, L), dtype=int)
color_ground = np.array([76, 66, 70]) / 255
color_trees = np.array([118, 176, 65]) / 255
color_fire = np.array([228, 87, 46]) / 255
cmap = ListedColormap([color_ground, color_trees, color_fire])

plt.figure(1)
for step in range(num_steps):
    next_grid = np.zeros((L, L), dtype=int)
    for r in range(L):
        for c in range(L):
            neighbor_is_burning = is_neighbor_burning(r, c, grid, L, BURNING)
            next_grid[r, c] = calculate_next_state(int(grid[r, c]), neighbor_is_burning, p, f, EMPTY, TREE, BURNING)
    grid = next_grid
    plt.clf()
    plt.imshow(grid, cmap=cmap, vmin=EMPTY, vmax=BURNING)
    plt.title(f"Forest Fire Model - Step {step + 1} / {num_steps}")
    plt.axis("off")
    plt.gca().set_aspect("equal")
    plt.pause(0.001)

plt.show()
