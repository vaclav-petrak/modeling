import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


sigma = 10
beta = 8 / 4
rho = 29


def system(_, a: np.ndarray) -> list[float]:
    return [
        -sigma * a[0] + sigma * a[1],
        rho * a[0] - a[1] - a[0] * a[2],
        -beta * a[2] + a[0] * a[1],
    ]


solution = solve_ivp(system, (0, 100), [1, 1, 1], max_step=0.01)
t = solution.t
a = solution.y.T

fig = plt.figure(1)
ax = fig.add_subplot(111, projection="3d")
ax.plot(a[:, 0], a[:, 1], a[:, 2])

plt.figure(2)
plt.plot(t, a[:, 1])
plt.show()
