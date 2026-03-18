import matplotlib.pyplot as plt
import numpy as np


beta = 0.3
n_total = 1000
i0 = 1
s0 = n_total - i0
t_max = 60
dt = 0.1

t = np.arange(0, t_max + dt, dt)
num_steps = len(t)
s = np.zeros(num_steps)
i = np.zeros(num_steps)
s[0] = s0
i[0] = i0

for step in range(1, num_steps):
    ds = -beta * s[step - 1] * i[step - 1] / n_total
    di = -ds
    s[step] = s[step - 1] + ds * dt
    i[step] = i[step - 1] + di * dt

plt.plot(t, s, "b", linewidth=2, label="Susceptible")
plt.plot(t, i, "r", linewidth=2, label="Infected")
plt.xlabel("Time (days)")
plt.ylabel("Number of individuals")
plt.legend()
plt.title("SI Model Simulation")
plt.show()
