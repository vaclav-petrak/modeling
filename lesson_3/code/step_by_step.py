import matplotlib.pyplot as plt
import numpy as np

from update_position import update_position


area = 100
population = 1000
infected = 10
iterations = 1500

position = np.random.randint(1, area + 1, size=(population, 2))
status = np.ones(population, dtype=int)
status[:infected] = 2

for _ in range(iterations):
    for person in range(population):
        x, y = update_position(int(position[person, 0]), int(position[person, 1]), area)
        position[person] = [x, y]

    plt.figure(1)
    plt.clf()
    plt.scatter(position[status == 1, 0], position[status == 1, 1], c="green", s=20)
    plt.scatter(position[status == 2, 0], position[status == 2, 1], c="red", s=20)
    plt.scatter(position[status == 3, 0], position[status == 3, 1], c="blue", s=20)
    plt.axis("square")
    plt.xlim(0, area)
    plt.ylim(0, area)
    plt.pause(0.001)

plt.show()
