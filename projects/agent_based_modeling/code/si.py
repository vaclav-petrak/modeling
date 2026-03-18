import random

import matplotlib.pyplot as plt
import numpy as np


area = 100
population = 1000
initial_infected = 1
iterations = 1500
infection_probability = 0.5

position = np.random.randint(1, area + 1, size=(population, 2))
status = np.ones(population, dtype=int)
status[:initial_infected] = 2

infected_count = np.zeros(iterations, dtype=int)
susceptible_count = np.zeros(iterations, dtype=int)


def move(x: int, y: int, area: int) -> tuple[int, int]:
    direction = random.randint(1, 4)
    if direction == 1 and y < area:
        y += 1
    elif direction == 2 and y > 1:
        y -= 1
    elif direction == 3 and x > 1:
        x -= 1
    elif direction == 4 and x < area:
        x += 1
    return x, y


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

for i in range(iterations):
    for person in range(population):
        if status[person] == 1:
            same_x = position[:, 0] == position[person, 0]
            same_y = position[:, 1] == position[person, 1]
            nearby_infected = same_x & same_y & (status == 2)
            if np.any(nearby_infected) and random.random() < infection_probability:
                status[person] = 2

    susceptible_count[i] = np.sum(status == 1)
    infected_count[i] = np.sum(status == 2)

    ax1.clear()
    ax1.scatter(position[status == 1, 0], position[status == 1, 1], c="green", s=15)
    ax1.scatter(position[status == 2, 0], position[status == 2, 1], c="red", s=15)
    ax1.set_xlim(0, area)
    ax1.set_ylim(0, area)
    ax1.set_aspect("equal")

    ax2.clear()
    ax2.plot(range(1, i + 2), susceptible_count[: i + 1], "g", linewidth=2)
    ax2.plot(range(1, i + 2), infected_count[: i + 1], "r", linewidth=2)
    ax2.set_title("S vs. I over time")
    ax2.set_xlim(1, iterations)
    ax2.set_ylim(0, population)
    plt.pause(0.001)

    for person in range(population):
        position[person] = move(int(position[person, 0]), int(position[person, 1]), area)

plt.show()
