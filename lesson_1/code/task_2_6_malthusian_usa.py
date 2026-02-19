import numpy as np
import matplotlib.pyplot as plt

# Parameters
r = 0.0275
start_year = 1790

# Time axis: equivalent to 0:10:230
t_usa = np.arange(0, 240, 10) 

# US population data (Millions)
P_usa = np.array([
    3.9, 5.3, 7.2, 9.6, 12.9, 17.1, 23.2, 31.4,
    38.6, 50.2, 63.0, 76.2, 92.2, 106.0, 123.2, 132.2,
    151.3, 179.3, 203.3, 226.5, 248.7, 281.4, 308.7, 331.4
])

# EXPLICIT SOLUTION
# P(t) = P0 * e^(rt)
P_expl = P_usa[0] * np.exp(r * t_usa)

# PLOTTING
years = t_usa + start_year
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Tile 1: Real data and model
ax1.plot(years, P_expl, color="red", label="Model")
ax1.plot(years, P_usa, color="black", label="Real Data")
ax1.set_title("Real data and model")
ax1.set_ylim(0, 350)
ax1.legend()

# Tile 2: The difference
ax2.plot(years, P_expl - P_usa, '-o', color="black")
ax2.set_title("The difference")

plt.tight_layout()
plt.show()