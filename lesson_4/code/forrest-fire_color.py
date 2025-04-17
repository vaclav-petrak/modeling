import numpy as np
import matplotlib.pyplot as plt

def detect_fire(row, col, grid):
    width, height = grid.shape
    neighborhood = grid[max(0,row-1):min(width,row+2), max(0,col-1):min(height,col+2)]
    return np.max(neighborhood) == 2

def update_cell_state(cell_state, fire_in_neighborhood, planting_chance, ignition_chance):
    if cell_state == 0:  # ground
        return int(np.random.random() < planting_chance)
    elif cell_state == 1:  # tree
        random_ignition = np.random.random() < ignition_chance
        return 2 if (fire_in_neighborhood or random_ignition) else 1
    elif cell_state == 2:  # fire
        return 0

# Initialize
area = 160
iterations = 1000
initial_coverage = 0.2
ignition_chance = 0.00002
planting_chance = 0.0040

# Colors
ground = np.array([76, 66, 70]) / 255
trees = np.array([118, 176, 65]) / 255
fire = np.array([228, 87, 46]) / 255

# Initial states
grid = (np.random.random((area, area)) < initial_coverage).astype(int)

# Memory allocation
tree_count = np.zeros(iterations)
fire_count = np.zeros(iterations)

# Set up the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
im = ax1.imshow(grid, cmap=plt.cm.colors.ListedColormap([ground, trees, fire]), vmin=0, vmax=2)
line_trees, = ax2.plot([], [], color=trees, linewidth=2)
line_fire, = ax2.plot([], [], color=fire, linewidth=2)
ax2.set_ylim(0, 12000)
ax2.set_xlim(0, iterations)
ax2.set_ylabel("Tree count")
ax2.set_xlabel("Time")
ax2.set_title("Forest fire simulation")

# Iterate
for i in range(iterations):
    new_grid = np.zeros((area, area), dtype=int)
    
    for row in range(area):
        for col in range(area):
            fire_in_neighborhood = detect_fire(row, col, grid)
            cell_state = grid[row, col]
            new_grid[row, col] = update_cell_state(cell_state, fire_in_neighborhood, planting_chance, ignition_chance)
    
    grid = new_grid
    
    # Summarize
    tree_count[i] = np.sum(grid == 1)
    fire_count[i] = np.sum(grid == 2)
    
    # Update plot
    im.set_data(grid)
    line_trees.set_data(range(i+1), tree_count[:i+1])
    line_fire.set_data(range(i+1), fire_count[:i+1] * 10)
    
    #plt.pause(0.05)

plt.show()