import numpy as np
import matplotlib.pyplot as plt

P0 = 2.50
r = 0.027
t_start, t_end, t_diff = 0, 70, 1

t_expl = np.arange(t_start, t_end + t_diff, t_diff)
P_expl = P0 * np.exp(r * t_expl)

plt.plot(t_expl, P_expl, linewidth=2)
plt.xlabel("Time (years)")
plt.ylabel("Population (millions)")
plt.ylim(0, 20)
plt.show()