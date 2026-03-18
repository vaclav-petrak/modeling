import random

import matplotlib.pyplot as plt
import numpy as np

from update_position import update_position


area = 100
population = 1000
infected = 10
iterations = 1500
infection_probability = 0.2
cure_constant = 0.03

position = np.random.randint(1, area + 1, size=(population, 2))
status = np.ones(population, dtype=int)
status[:infected] = 2

infected_count = np.zeros(iterations, dtype=int)
susceptible_count = np.zeros(iterations, dtype=int)
recovered_count = np.zeros(iterations, dtype=int)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

for i in range(iterations):
    for person in range(population):
        if status[person] == 1:
            same_x = position[:, 0] == position[person, 0]
            same_y = position[:, 1] == position[person, 1]
            same_square_and_infected = same_x & same_y & (status == 2)
            if np.any(same_square_and_infected) and random.random() < infection_probability:
                status[person] = 2
        elif status[person] == 2 and random.random() < cure_constant:
            status[person] = 3

    infected_count[i] = np.sum(status == 2)
    susceptible_count[i] = np.sum(status == 1)
    recovered_count[i] = np.sum(status == 3)

    ax1.clear()
    ax1.scatter(position[status == 1, 0], position[status == 1, 1], c="green", s=15)
    ax1.scatter(position[status == 2, 0], position[status == 2, 1], c="red", s=15)
    ax1.scatter(position[status == 3, 0], position[status == 3, 1], c="blue", s=15)
    ax1.set_xlim(0, area)
    ax1.set_ylim(0, area)
    ax1.set_aspect("equal")

    ax2.clear()
    ax2.plot(range(1, i + 2), susceptible_count[: i + 1], color="green", linewidth=2)
    ax2.plot(range(1, i + 2), infected_count[: i + 1], color="red", linewidth=2)
    ax2.plot(range(1, i + 2), recovered_count[: i + 1], color="blue", linewidth=2)
    ax2.set_xlim(1, iterations)
    plt.pause(0.001)

    for person in range(population):
        position[person] = update_position(int(position[person, 0]), int(position[person, 1]), area)

plt.show()
