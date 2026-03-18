import matplotlib.pyplot as plt
import numpy as np


r = 1.75
x0 = 0.25
n_total = 30

x = np.zeros(n_total + 1)
x[0] = x0
for i in range(n_total):
    x[i + 1] = r * (1 - x[i]) * x[i]

x_n = x[:-1]
x_n_plus_1 = x[1:]
x_plot = np.arange(0, 1.01, 0.01)
y_plot = r * x_plot * (1 - x_plot)

for i in range(1, n_total + 1):
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(x_plot, y_plot, color="blue", linewidth=2)
    ax1.plot([0, 1], [0, 1], color="black", linewidth=2)
    ax1.step(x_n[:i], x_n_plus_1[:i], color="red", linewidth=1, where="pre")
    ax1.plot([x_n[0], x_n[0]], [0, x_n_plus_1[0]], color="red", linewidth=1)
    ax1.set_aspect("equal")
    ax2.plot(x_n[:i], linewidth=1, color="red")
    ax2.set_ylim(0, 1)
    ax2.set_xlim(0, n_total)
    plt.pause(0.1)
    plt.close(fig)
