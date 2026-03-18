import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


f = np.array([0, 1.6, 0.8], dtype=float)
s = np.array([0.5, 0.7], dtype=float)
num_age_classes = len(f)

L = np.zeros((num_age_classes, num_age_classes))
L[0, :] = f
for i in range(num_age_classes - 1):
    L[i + 1, i] = s[i]

print("Leslie Matrix (L):")
print(L)

N0 = np.array([10, 8, 5], dtype=float)
print("Initial Population Vector (N0):")
print(N0)

N1 = L @ N0
print("Population Vector at t=1 (N1):")
print(N1)

num_time_steps = 20
population_history = np.zeros((num_age_classes, num_time_steps + 1))
population_history[:, 0] = N0

Nt = N0.copy()
for t in range(num_time_steps):
    Nt = L @ Nt
    population_history[:, t + 1] = Nt

total_population = np.sum(population_history, axis=0)
age_structure = np.zeros_like(population_history)
for t in range(population_history.shape[1]):
    if total_population[t] > 0:
        age_structure[:, t] = population_history[:, t] / total_population[t]

fig1, ax1 = plt.subplots()
ax1.plot(np.arange(num_time_steps + 1), total_population, "b-o", linewidth=1.5)
ax1.set_xlabel("Time Step (Years)")
ax1.set_ylabel("Total Population Size")
ax1.set_title("Total Population Growth Over Time")
ax1.grid(True)

fig2, ax2 = plt.subplots()
ax2.stackplot(np.arange(num_time_steps + 1), age_structure[0], age_structure[1], age_structure[2], labels=["Age Class 1", "Age Class 2", "Age Class 3"])
ax2.set_xlabel("Time Step (Years)")
ax2.set_ylabel("Proportion of Population")
ax2.set_title("Population Age Structure Over Time")
ax2.legend(loc="upper right")
ax2.set_ylim(0, 1)

eigenvalues, eigenvectors = np.linalg.eig(L)
idx = np.argmax(np.real(eigenvalues))
dominant_eigenvalue = np.real(eigenvalues[idx])
dominant_eigenvector = np.real(eigenvectors[:, idx])
stable_age_distribution = dominant_eigenvector / np.sum(dominant_eigenvector)

print(f"Dominant Eigenvalue (lambda): {dominant_eigenvalue:.4f}")
print("Stable Age Distribution (Proportions):")
print(stable_age_distribution)
print("Simulated Age Structure at final time step:")
print(age_structure[:, -1])

fig3, ax3 = plt.subplots()


def update(frame: int) -> None:
    ax3.clear()
    ax3.barh(range(num_age_classes), population_history[:, frame], height=0.5, color=[[0.2, 0.4, 0.6]])
    ax3.set_xlim(0, np.max(population_history) * 1.1)
    ax3.set_yticks(range(num_age_classes))
    ax3.set_yticklabels(["Age Class 1", "Age Class 2", "Age Class 3"])
    ax3.invert_yaxis()
    ax3.set_xlabel("Number of Individuals")
    ax3.set_title(f"Population Age Tree - Year {frame}")
    ax3.grid(True, axis="x")


animation.FuncAnimation(fig3, update, frames=num_time_steps + 1, interval=200, repeat=False)
plt.show()
