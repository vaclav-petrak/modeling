import matplotlib.pyplot as plt
import numpy as np


points = 2000
iterations = 100
x = np.linspace(-2, 1, points)
y = np.linspace(-1.5, 1.5, points)
xx, yy = np.meshgrid(x, y)
c = xx + 1j * yy
z = np.zeros_like(c)
divergence = np.zeros(c.shape, dtype=int)

plt.figure(figsize=(10, 10))
for _ in range(iterations):
    z = z ** 2 + c
    divergence[np.abs(z) > 2] = 1
    plt.clf()
    plt.imshow(divergence, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="gray")
    plt.pause(0.001)

plt.show()
