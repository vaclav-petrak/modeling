import numpy as np
import matplotlib.pyplot as plt

# Parameters and Time
P0, r, K = 3.9, 0.0255, 430
t = np.arange(0, 400, 1/12)

# Vectorized Logistic Growth (Analytical Solution)
# P(t) = K / (1 + ((K - P0) / P0) * exp(-rt))
P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))
P_diff = r * P * (1 - P / K) * (1/12)

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
plots = [
    (t, P, "Population vs Time"),
    (t, P_diff, "Growth Amount vs Time"),
    (P, P_diff / P, "Per Capita Growth vs Pop"),
    (P, P_diff, "Growth Amount vs Pop")
]

for ax, (x, y, title) in zip(axs.flat, plots):
    ax.plot(x, y)
    ax.set_title(title)

plt.tight_layout()
plt.show()