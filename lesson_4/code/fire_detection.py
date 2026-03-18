import numpy as np


forest = np.array([
    [0, 1, 1, 0, 2],
    [0, 1, 1, 1, 1],
    [0, 2, 0, 1, 1],
    [1, 1, 0, 0, 0],
])


def detect_fire(row: int, col: int, grid: np.ndarray) -> bool:
    width, height = grid.shape
    neighborhood = grid[max(0, row - 1):min(width, row + 2), max(0, col - 1):min(height, col + 2)]
    return np.max(neighborhood) == 2


print(detect_fire(1, 1, forest))
print(detect_fire(3, 4, forest))
print(detect_fire(0, 4, forest))
print(detect_fire(0, 4, forest))
