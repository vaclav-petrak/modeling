import matplotlib.pyplot as plt
import numpy as np


def create_random_corridor_network(grid_size: int = 100, num_segments: int = 200, segment_length: int = 5, turn_probability: float = 0.3) -> np.ndarray:
    corridor_network = np.zeros((grid_size, grid_size), dtype=int)
    current_x = np.random.randint(0, grid_size)
    current_y = np.random.randint(0, grid_size)
    corridor_network[current_y, current_x] = 1
    directions = np.array([[-1, 0], [1, 0], [0, 1], [0, -1]])
    current_direction_idx = np.random.randint(0, 4)

    for _ in range(num_segments):
        if np.random.random() < turn_probability:
            current_direction_idx = np.random.randint(0, 4)
        current_direction = directions[current_direction_idx]
        for _ in range(segment_length):
            new_x = current_x + current_direction[1]
            new_y = current_y + current_direction[0]
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                current_x = new_x
                current_y = new_y
                corridor_network[current_y, current_x] = 1
            else:
                current_direction_idx = np.random.randint(0, 4)
                break
    return corridor_network


grid_size = 100
num_segments = 200
segment_length = 7
turn_probability = 0.25
corridor_map = create_random_corridor_network(grid_size, num_segments, segment_length, turn_probability)
plt.imshow(corridor_map, cmap="gray")
plt.title("Random Corridor Network")
plt.axis("off")
plt.show()
