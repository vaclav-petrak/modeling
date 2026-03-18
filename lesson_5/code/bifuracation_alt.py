import matplotlib.pyplot as plt
import numpy as np


r = np.linspace(0, 4, 20000)
n_total = 2000
x = 0.5 * np.ones_like(r)

for _ in range(n_total):
    x = r * x * (1 - x)

plt.figure(1)
for _ in range(50):
    x = r * x * (1 - x)
    plt.plot(r, x, ".", color="black", markersize=0.01)
    plt.xlim(2.8, 4)
    plt.xlabel("r")
    plt.ylabel("x")
    plt.pause(1)

plt.savefig("Bifurcation.png")
plt.show()
