import matplotlib.pyplot as plt
import numpy as np


steps = 100000
boundary = 500
point = np.zeros((2, steps), dtype=int)
point2 = np.zeros((2, steps), dtype=int)


def update_position(pos_current: np.ndarray, boundary: int) -> np.ndarray:
    x, y = int(pos_current[0]), int(pos_current[1])
    direction = np.random.randint(1, 5)
    if direction == 1 and y < boundary:
        y += 1
    elif direction == 2 and y > -boundary:
        y -= 1
    elif direction == 3 and x > -boundary:
        x -= 1
    elif direction == 4 and x < boundary:
        x += 1
    return np.array([x, y])


for i in range(steps - 1):
    point[:, i + 1] = update_position(point[:, i], boundary)
    point2[:, i + 1] = update_position(point2[:, i], boundary)

plt.plot(point[0, :], point[1, :])
plt.plot(point2[0, :], point2[1, :], color=(180 / 255, 70 / 255, 87 / 255))
plt.plot(point[0, -1], point[1, -1], "bo", markerfacecolor="red")
plt.plot(point2[0, -1], point2[1, -1], "bo", markerfacecolor="red")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis("square")
plt.xlim(-boundary, boundary)
plt.ylim(-boundary, boundary)
plt.show()
