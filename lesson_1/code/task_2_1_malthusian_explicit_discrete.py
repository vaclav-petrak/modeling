import numpy as np

P0 = 2.5   # Initial population
r = 0.027  # Growth rate 2.7%

t_task1 = np.array([1, 5, 7.5, 25.78])

print("Years of interest:")
print(t_task1)
print("Calculated population size:")
print(P0 * np.exp(r * t_task1))