import matplotlib.pyplot as plt
import numpy as np


def update_grain_position(grid: np.ndarray, new_grid: np.ndarray, row: int, col: int) -> np.ndarray:
    if grid[row + 1, col] == 0:
        new_grid[row, col] = 0
        new_grid[row + 1, col] = 1
    elif grid[row + 1, col - 1] == 0:
        new_grid[row, col] = 0
        new_grid[row + 1, col - 1] = 1
    elif grid[row + 1, col + 1] == 0:
        new_grid[row, col] = 0
        new_grid[row + 1, col + 1] = 1
    return new_grid


def generate_new_grain(grid: np.ndarray, grid_size: int) -> np.ndarray:
    plot_center = round(grid_size / 2)
    random_variation = np.random.randint(-5, 6)
    stream_distance = round(grid_size / 5)
    stream_position_start = np.array([2, 1, 1, 1, -1, -1])
    stream = stream_distance * np.random.choice(stream_position_start)
    grain_start = plot_center + stream + random_variation
    grain_start = max(0, min(grid_size - 1, grain_start))
    grid[0, grain_start] = 1
    return grid


grid_size = 100
grain_count = 0
grid = np.zeros((grid_size, grid_size), dtype=int)
plt.figure(1)
plt.axis("off")

while grain_count < round(grid_size ** 2 / 4):
    new_grid = grid.copy()
    for row in range(grid_size - 2, -1, -1):
        for col in range(1, grid_size - 1):
            if grid[row, col] == 1:
                new_grid = update_grain_position(grid, new_grid, row, col)
    grid = new_grid
    grid = generate_new_grain(grid, grid_size)
    grain_count = int(np.sum(grid))
    plt.clf()
    plt.imshow(grid, cmap="gray_r")
    plt.axis("off")
    plt.pause(0.001)

plt.show()
