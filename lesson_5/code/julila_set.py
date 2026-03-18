import matplotlib.pyplot as plt
import numpy as np


points = 1000
iterations = 10
x = np.linspace(-2, 2, points)
y = np.linspace(-2, 2, points)
real, imag = np.meshgrid(x, y)
c = real + 1j * imag
z = c.copy()
escape_time = np.zeros_like(real)

plt.figure(figsize=(10, 10))
for _ in range(iterations):
    bounded = np.abs(z) <= 2
    z[bounded] = z[bounded] ** 2
    escape_time[bounded] += 1
    plt.clf()
    plt.imshow(escape_time, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="jet")
    plt.pause(0.5)

plt.show()
