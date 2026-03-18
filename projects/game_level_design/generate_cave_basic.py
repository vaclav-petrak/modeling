import matplotlib.pyplot as plt
import numpy as np


grid_width = 100
grid_height = grid_width
initial_wall_chance = 0.54
simulation_steps = 5
seed = 1
wall_death_limit = 4
wall_birth_limit = 5

rng = np.random.default_rng(seed)
random_grid = rng.random((grid_height, grid_width))
map_grid = np.zeros((grid_height, grid_width), dtype=int)
map_grid[random_grid < initial_wall_chance] = 1

for step in range(simulation_steps):
    new_map = map_grid.copy()
    for y in range(1, grid_height - 1):
        for x in range(1, grid_width - 1):
            neighbors = map_grid[y - 1:y + 2, x - 1:x + 2]
            wall_count = int(np.sum(neighbors) - map_grid[y, x])
            if map_grid[y, x] == 1:
                if wall_count < wall_death_limit:
                    new_map[y, x] = 0
            else:
                if wall_count > wall_birth_limit:
                    new_map[y, x] = 1
    map_grid = new_map
    print(f"Step {step + 1} complete.")

map_grid[0, :] = 1
map_grid[-1, :] = 1
map_grid[:, 0] = 1
map_grid[:, -1] = 1

plt.imshow(map_grid, cmap="gray_r")
plt.title("Generated Cave Map")
plt.axis("off")
plt.gca().set_aspect("equal")
plt.show()
