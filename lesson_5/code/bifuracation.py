import matplotlib.pyplot as plt
import numpy as np


r = np.linspace(2.9, 4, 80000)
n_initial = 2000
n_plotting = 100
x = 0.5 * np.ones_like(r)

for _ in range(n_initial):
    x = r * x * (1 - x)

plt.figure(1)
for _ in range(n_plotting):
    x = r * x * (1 - x)
    plt.plot(r, x, ".", color="black", markersize=0.01)

plt.xlim(2.9, 4)
plt.xlabel("r")
plt.ylabel("x")
plt.show()
