import matplotlib.pyplot as plt
import numpy as np


num_generations = 10
r0 = 1.5
initial_infections = 1

num_infections = np.zeros(num_generations, dtype=int)
num_infections[0] = initial_infections

for generation in range(1, num_generations):
    current_infections = 0
    for _ in range(num_infections[generation - 1]):
        current_infections += np.random.poisson(r0)
    num_infections[generation] = current_infections

print("Generation  Infections")
for generation, infections in enumerate(num_infections, start=1):
    print(generation, infections)

plt.bar(np.arange(1, num_generations + 1), num_infections)
plt.xlabel("Generation")
plt.ylabel("Number of Infections")
plt.title("Disease Spread using Branching Process")
plt.show()
