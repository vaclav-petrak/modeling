import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation

# --- YOUR ORIGINAL PARAMETERS 
GRID_SIZE = 160
TOTAL_STEPS = 500
PROB_SPONTANEOUS_IGNITION = 0.00002
PROB_TREE_GROWTH = 0.004

STATE_EMPTY = 0
STATE_TREE = 1
STATE_BURNING = 2


def is_neighbor_burning(row, col, forest_grid, grid_size, state_burning):
    """Checks the 8 surrounding cells (Moore neighborhood) for fire."""
    for row_offset in [-1, 0, 1]:
        for col_offset in [-1, 0, 1]:
            if row_offset == 0 and col_offset == 0:
                continue
            neighbor_row = row + row_offset
            neighbor_col = col + col_offset
            is_within_bounds = (0 <= neighbor_row < grid_size) and (0 <= neighbor_col < grid_size)
            if is_within_bounds:
                if forest_grid[neighbor_row, neighbor_col] == state_burning:
                    return True
    return False

def calculate_next_state(current_state, is_fire_nearby, prob_growth, prob_ignition, state_empty, state_tree, state_burning):
    """Determines what happens to a specific cell in the next time step."""
    if current_state == state_empty:
        if np.random.rand() < prob_growth:
            return state_tree
        else:
            return state_empty
    elif current_state == state_tree:   
        random_ignition_occurred = np.random.rand() < prob_ignition
        if is_fire_nearby or random_ignition_occurred:
            return state_burning
        else:
            return state_tree
    elif current_state == state_burning: 
        return state_empty
    else: 
        return current_state

# --- VISUALIZATION ADJUSTED FOR VS CODE ---
forest_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int) 

# We use the interactive mode or a standard plot window for VS Code
fig, ax = plt.subplots(figsize=(6, 6))

color_ground = [76/255,  66/255,  70/255]  
color_trees  = [118/255, 176/255,  65/255] 
color_fire   = [228/255,  87/255,  46/255] 
forest_cmap = ListedColormap([color_ground, color_trees, color_fire])

image_display_handle = ax.imshow(forest_grid, cmap=forest_cmap, vmin=STATE_EMPTY, vmax=STATE_BURNING)
ax.axis('off')

def update_forest(frame_number):
    global forest_grid 
    future_forest_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int) 
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE): 
            is_fire_nearby = is_neighbor_burning(row, col, forest_grid, GRID_SIZE, STATE_BURNING)
            current_state = forest_grid[row, col]
            
            future_forest_grid[row, col] = calculate_next_state(
                current_state, is_fire_nearby, PROB_TREE_GROWTH, 
                PROB_SPONTANEOUS_IGNITION, STATE_EMPTY, STATE_TREE, STATE_BURNING
            )

    forest_grid = future_forest_grid.copy() 
    image_display_handle.set_data(forest_grid)
    ax.set_title(f'Forest Fire Model')
    return [image_display_handle]

forest_animation = animation.FuncAnimation(fig, update_forest, frames=TOTAL_STEPS, interval=50, blit=True, repeat=False)

# This is the key change for VS Code/Desktop:
plt.show()