import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# =============================================================================
# Leslie Matrix Population Model Implementation
# =============================================================================

# Step 1: Define Parameters
# Fecundity rates (average offspring per individual in each age class)
f = np.array([0, 1.6, 0.8])  # f1=0, f2=1.6, f3=0.8

# Survival rates (probability of surviving to the next age class)
s = np.array([0.5, 0.7])  # s1=0.5 (age 1->2), s2=0.7 (age 2->3)
num_age_classes = len(f)   # Number of age classes (k=3)

# Step 2: Construct the Leslie Matrix (L)
L = np.zeros((num_age_classes, num_age_classes))

# Fill the first row with fecundity rates
L[0, :] = f

# Fill the sub-diagonal with survival rates
for i in range(num_age_classes - 1):
    L[i + 1, i] = s[i]

print("Leslie Matrix (L):")
print(L)

# Step 3: Define the Initial Population Vector (N0)
N0 = np.array([10, 8, 5], dtype=float)  # [n1, n2, n3] at time t=0
print("\nInitial Population Vector (N0):")
print(N0)

# Step 4: Project the Population for One Time Step
N1 = L @ N0  # Calculate population at time t=1
print("\nPopulation Vector at t=1 (N1):")
print(N1)

# Step 5: Simulate Population Growth Over Multiple Time Steps
num_time_steps = 20
population_history = np.zeros((num_age_classes, num_time_steps + 1))
population_history[:, 0] = N0

Nt = N0.copy()
for t in range(num_time_steps):
    Nt_plus_1 = L @ Nt
    population_history[:, t + 1] = Nt_plus_1
    Nt = Nt_plus_1

# Step 6: Analyze and Visualize Results
# Calculate total population size at each time step
total_population = population_history.sum(axis=0)

# Calculate age structure (proportions) over time
age_structure = np.zeros_like(population_history)
for t in range(population_history.shape[1]):
    if total_population[t] > 0:
        age_structure[:, t] = population_history[:, t] / total_population[t]

time_axis = np.arange(num_time_steps + 1)

# Plot 1: Total population size
fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(time_axis, total_population, 'b-o', linewidth=1.5)
ax1.set_xlabel("Time Step (Years)")
ax1.set_ylabel("Total Population Size")
ax1.set_title("Total Population Growth Over Time")
ax1.grid(True)
plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/total_population.png", dpi=150)
plt.show()

# Plot 2: Age structure over time (stacked area)
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.stackplot(
    time_axis,
    age_structure[0], age_structure[1], age_structure[2],
    labels=["Age Class 1", "Age Class 2", "Age Class 3"]
)
ax2.set_xlabel("Time Step (Years)")
ax2.set_ylabel("Proportion of Population")
ax2.set_title("Population Age Structure Over Time")
ax2.legend(loc="upper right")
ax2.set_ylim(0, 1)
plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/age_structure.png", dpi=150)
plt.show()

# Step 7: Eigenvalue Analysis
eigenvalues, eigenvectors = np.linalg.eig(L)

# Find the dominant eigenvalue (largest real part)
idx = np.argmax(np.real(eigenvalues))
dominant_eigenvalue = np.real(eigenvalues[idx])
dominant_eigenvector = np.real(eigenvectors[:, idx])

# Normalize the stable age distribution so elements sum to 1
stable_age_distribution = dominant_eigenvector / dominant_eigenvector.sum()

print(f"\nDominant Eigenvalue (lambda): {dominant_eigenvalue:.4f}")
print("Stable Age Distribution (Proportions):")
print(stable_age_distribution)
print("Simulated Age Structure at final time step:")
print(age_structure[:, -1])

# Step 8: Animated Age Pyramid
fig3, ax3 = plt.subplots(figsize=(7, 4))
colors = [0.2, 0.4, 0.6]

def update(frame):
    ax3.cla()
    values = population_history[:, frame]
    bars = ax3.barh(
        range(num_age_classes), values, height=0.5,
        color=[[0.2, 0.4, 0.6]]
    )
    ax3.set_xlim(0, population_history.max() * 1.1)
    ax3.set_yticks(range(num_age_classes))
    ax3.set_yticklabels(["Age Class 1", "Age Class 2", "Age Class 3"])
    ax3.invert_yaxis()  # Youngest at top
    ax3.set_xlabel("Number of Individuals")
    ax3.set_title(f"Population Age Tree — Year {frame}")
    ax3.grid(True, axis='x')

ani = animation.FuncAnimation(
    fig3, update, frames=num_time_steps + 1, interval=200, repeat=False
)
plt.tight_layout()

# Save animation as GIF
ani.save("/mnt/user-data/outputs/age_pyramid.gif", writer="pillow", fps=5)
plt.show()

print("\nDone! Plots saved to outputs.")