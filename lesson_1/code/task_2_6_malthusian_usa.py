import numpy as np
import matplotlib.pyplot as plt

# Growth rate
r = 0.027

# Start year
start_year = 1950

# Time axis (years)
t_sen = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 72, 73, 74])

# Senegalese population (millions)
P_sen = np.array([2.5, 2.8, 3.3, 3.8, 4.4, 5.0, 5.7, 6.5, 7.5, 8.6, 9.7, 11.0, 12.5, 14.4, 16.4, 17.3, 17.8, 18.2])

# EXPLICIT SOLUTION
# Initial population is the first value: P_sen[0]
P_expl = P_sen[0] * np.exp(r * t_sen)

# PLOTTING
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Tile 1: Real data and model
ax1.plot(t_sen + start_year, P_expl, color="red", label='Model')
ax1.plot(t_sen + start_year, P_sen, color="blue", label='Real Data')
ax1.set_title("Real data and model")
ax1.set_ylim(0, 20)
ax1.legend()

# Tile 2: The difference
ax2.plot(t_sen + start_year, P_expl - P_sen, '-o', color="black")
ax2.set_title("The difference")

plt.tight_layout()
plt.show()