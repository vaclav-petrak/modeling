import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


area = 100
initial_coverage = 0
iterations = 200
step_time = 0.05

dead = np.array([238, 243, 106]) / 255
live = np.array([63, 48, 71]) / 255
pattern = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 0, 1],
])


def place_pattern(grid: np.ndarray, pattern: np.ndarray, position: tuple[int, int]) -> np.ndarray:
    h, w = pattern.shape
    row, col = position
    grid[row:row + h, col:col + w] = pattern
    return grid


def get_neighbors_alive(row: int, col: int, grid: np.ndarray) -> int:
    width, height = grid.shape
    cell_with_neighborhood = grid[max(0, row - 1):min(width, row + 2), max(0, col - 1):min(height, col + 2)]
    return int(np.sum(cell_with_neighborhood) - grid[row, col])


def update_cell_state(is_alive: int, neighbors_alive: int) -> int:
    if is_alive and neighbors_alive < 2:
        return 0
    if is_alive and neighbors_alive in (2, 3):
        return 1
    if is_alive and neighbors_alive > 3:
        return 0
    if not is_alive and neighbors_alive == 3:
        return 1
    return 0


grid = (np.random.random((area, area)) < initial_coverage).astype(int)
grid = place_pattern(grid, pattern, (50, 50))

for i in range(iterations):
    new_grid = np.zeros((area, area), dtype=int)
    for row in range(area):
        for col in range(area):
            neighbors_alive = get_neighbors_alive(row, col, grid)
            new_grid[row, col] = update_cell_state(int(grid[row, col]), neighbors_alive)
    grid = new_grid
    plt.figure(1)
    plt.clf()
    plt.imshow(grid, cmap=ListedColormap([live, dead]))
    plt.axis("off")
    plt.title(f"Iteration {i + 1}")
    plt.pause(step_time)

plt.show()
