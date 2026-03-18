from collections import deque

import matplotlib.pyplot as plt
import numpy as np


def run_simulation_step(map_grid: np.ndarray, death_limit: int, birth_limit: int) -> np.ndarray:
    grid_height, grid_width = map_grid.shape
    new_map = map_grid.copy()
    for y in range(1, grid_height - 1):
        for x in range(1, grid_width - 1):
            neighbors = map_grid[y - 1:y + 2, x - 1:x + 2]
            wall_count = int(np.sum(neighbors) - map_grid[y, x])
            if map_grid[y, x] == 1:
                if wall_count < death_limit:
                    new_map[y, x] = 0
            else:
                if wall_count > birth_limit:
                    new_map[y, x] = 1
    return new_map


def enforce_border_walls(map_grid: np.ndarray) -> np.ndarray:
    map_with_border = map_grid.copy()
    map_with_border[0, :] = 1
    map_with_border[-1, :] = 1
    map_with_border[:, 0] = 1
    map_with_border[:, -1] = 1
    return map_with_border


def keep_largest_floor_area(map_grid: np.ndarray) -> np.ndarray:
    grid_height, grid_width = map_grid.shape
    visited = np.zeros((grid_height, grid_width), dtype=bool)
    largest_component_cells: list[tuple[int, int]] = []
    max_area = 0

    for r in range(grid_height):
        for c in range(grid_width):
            if map_grid[r, c] == 0 and not visited[r, c]:
                current_component_cells: list[tuple[int, int]] = []
                queue: deque[tuple[int, int]] = deque([(r, c)])
                visited[r, c] = True
                while queue:
                    curr_r, curr_c = queue.popleft()
                    current_component_cells.append((curr_r, curr_c))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        next_r = curr_r + dr
                        next_c = curr_c + dc
                        if 0 <= next_r < grid_height and 0 <= next_c < grid_width:
                            if map_grid[next_r, next_c] == 0 and not visited[next_r, next_c]:
                                visited[next_r, next_c] = True
                                queue.append((next_r, next_c))
                if len(current_component_cells) > max_area:
                    max_area = len(current_component_cells)
                    largest_component_cells = current_component_cells

    modified_map = np.ones((grid_height, grid_width), dtype=int)
    for row, col in largest_component_cells:
        modified_map[row, col] = 0
    return modified_map


grid_width = 100
grid_height = grid_width
initial_wall_chance = 0.535
simulation_steps = 15
seed = 3
wall_death_limit = 4
wall_birth_limit = 5

rng = np.random.default_rng(seed)
random_grid = rng.random((grid_height, grid_width))
map_grid = np.zeros((grid_height, grid_width), dtype=int)
map_grid[random_grid < initial_wall_chance] = 1

for _ in range(simulation_steps):
    map_grid = run_simulation_step(map_grid, wall_death_limit, wall_birth_limit)

map_grid = keep_largest_floor_area(map_grid)
map_grid = enforce_border_walls(map_grid)

plt.imshow(map_grid, cmap="gray_r")
plt.axis("off")
plt.gca().set_aspect("equal")
plt.show()
