import numpy as np
import matplotlib.pyplot as plt

# Parameters
r, P0, K, start_year = 0.0237, 5.2, 460, 1790
t_usa = np.arange(0, 240, 10)
P_usa = np.array([3.9, 5.3, 7.2, 9.6, 12.9, 17.1, 23.2, 31.4, 38.6, 50.2, 63.0, 76.2, 92.2, 106.0, 123.2, 132.2, 151.3, 179.3, 203.3, 226.5, 248.7, 281.4, 308.7, 331.4])

dt = 1/12
t_num = np.arange(0, 230 + dt, dt)
P_num = np.zeros(len(t_num))
P_num[0] = P0

for i in range(len(t_num) - 1):
    P_num[i+1] = P_num[i] + r * P_num[i] * (1 - P_num[i] / K) * dt

# Plotting
plt.plot(t_num + start_year, P_num, 'r-', label='Logistic Model')
plt.plot(t_usa + start_year, P_usa, 'ko', label='Real Data')
plt.axis([1790, 2020, 0, 350])
plt.legend(); plt.title("USA Population: Logistic Growth Model")
plt.xlabel("Year"); plt.ylabel("Population (millions)")
plt.show()