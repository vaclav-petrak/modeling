import matplotlib.pyplot as plt
import numpy as np


r = 0.5
k = 200
a_strong = 60
n = np.linspace(0, k * 1.05, 5000)

growth_no = r * n * (1 - n / k)
growth_weak = (r / k) * n ** 2 * (1 - n / k)
growth_strong = r * n * (1 - n / k) * (n / a_strong - 1)

plt.plot(n, growth_no, linewidth=2, label="No Allee Effect")
plt.plot(n, growth_weak, linewidth=2, label="Weak Allee Effect")
plt.plot(n, growth_strong, linewidth=2, label="Strong Allee Effect")
plt.axhline(0, color="black", linewidth=1.5)
plt.title("Population Growth Models with Allee Effects")
plt.xlabel("Population Density")
plt.ylabel("dN/dt")
plt.xlim(0, k * 1.1)
plt.legend(loc="lower right")
plt.show()
