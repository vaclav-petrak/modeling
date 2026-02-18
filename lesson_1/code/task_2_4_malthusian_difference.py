import numpy as np
import matplotlib.pyplot as plt

# MODELING PARAMETERS
P0, r = 2.50,  0.027
start_year = 1950
t_start, t_end, t_diff = 0, 70, 1

# EXPLICIT SOLUTION
t_expl = np.arange(t_start, t_end + t_diff, t_diff)
P_expl = P0 * np.exp(r * t_expl)

# NUMERICAL SOLUTION
t_num = [t_start]
P_num = [P0]
for i in range(int(t_end/t_diff)):
    P_num.append(P_num[i] + r * P_num[i] * t_diff)
    t_num.append(t_num[i] + t_diff)
P_num = np.array(P_num)
t_num = np.array(t_num)

# PLOTTING
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Explicit vs Numerical
ax1.plot(t_expl + start_year, P_expl, color="red", label="Explicit")
ax1.plot(t_num + start_year, P_num, color="blue", label="Numerical")
ax1.set_title("Explicit and numerical solution")
ax1.set_ylim(0, 20)
ax1.set_xlim(1950, 2020)
ax1.legend()

# Plot 2: Difference
ax2.plot(t_expl + start_year, P_expl - P_num, color="black")
ax2.set_title("The difference")
ax2.set_ylim(0, 0.5)
ax2.set_xlim(1950, 2020)

plt.tight_layout()
plt.show()