import numpy as np
import matplotlib.pyplot as plt

# Params & Time
P0, r, K, dt = 3.9, 0.0255, 430, 1/12
t = np.arange(0, 400 + dt, dt)
P = np.zeros(len(t))
P[0] = P0

for i in range(len(t) - 1):
    P[i+1] = P[i] + r * P[i] * (1 - P[i] / K) * dt

# Derived Data
P_diff = np.concatenate([[np.nan], np.diff(P)])
plots = [(t, P, "Pop vs Time"), (t, P_diff, "Growth vs Time"),  (P, P_diff/P, "Per Capita vs Pop"), (P, P_diff, "Growth vs Pop")]

fig, axs = plt.subplots(2, 2, figsize=(10, 7))
for ax, (x, y, title) in zip(axs.flat, plots):
    ax.plot(x, y)
    ax.set_title(title)

plt.tight_layout()
plt.show()