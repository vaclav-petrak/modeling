import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Leslie Matrix Population Model
# =============================================================================

# --- Model Parameters ---
group_interval = 5
simulation_years = 100
initial_year = 2010

# Initial population vector
population_initial = np.array([
    275413, 228558, 223394, 300086, 339507, 365668,
    450984, 410637, 341023, 333977, 351237, 390758,
    380115, 293910, 212293, 196457, 149630,  84217,
     16110,   5079
], dtype=float)

# Annual survival rates per year
survival_annual = np.array([
    0.999354, 0.999891, 0.999888, 0.999783, 0.999747, 0.999751,
    0.999643, 0.999437, 0.998944, 0.998111, 0.996996, 0.995222,
    0.992205, 0.987149, 0.978713, 0.962139, 0.925109, 0.857950,
    0.743265
])

# Fertility rates per year
fertility_annual = np.array([
    0.000000, 0.000000, 0.000027, 0.005455, 0.022008, 0.048309,
    0.047481, 0.019136, 0.002915, 0.000117, 0.000006, 0.000000,
    0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000,
    0.000000, 0.000000
])

# --- Initialisation ---
simulation_steps = simulation_years // group_interval

# Adjust annual rates to match group interval
survival_group  = survival_annual ** group_interval
fertility_group = fertility_annual * group_interval

# --- Build Leslie Matrix ---
n = len(population_initial)
leslie_matrix = np.zeros((n, n))
leslie_matrix[0, :] = fertility_group
for i in range(1, n):
    leslie_matrix[i, i - 1] = survival_group[i - 1]

# --- Run Simulation ---
population_by_step = np.zeros((n, simulation_steps + 1))
population_by_step[:, 0] = population_initial

for t in range(1, simulation_steps + 1):
    population_by_step[:, t] = leslie_matrix @ population_by_step[:, t - 1]

# --- Analysis ---
total_population = population_by_step.sum(axis=0)

# --- Plotting ---
year_axis = np.arange(
    initial_year,
    initial_year + (simulation_steps + 1) * group_interval,
    group_interval
)

# Build age group labels
age_labels = []
for i in range(n - 1):
    age_labels.append(f"{i * group_interval}–{(i + 1) * group_interval - 1}")
age_labels.append(f"{(n - 1) * group_interval}+")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Total population over time
ax1.plot(year_axis, total_population, '-o', linewidth=2, markersize=4)
ax1.set_xlabel("Year")
ax1.set_ylabel("Total Population")
ax1.set_title(f"Population Development ({group_interval}-Year Leslie Model)")
ax1.set_ylim(0, total_population.max() * 1.1)
ax1.grid(True)

# Right: Initial vs Final age structure
y_pos = np.arange(n)
bar_width = 0.4

bars1 = ax2.barh(y_pos - bar_width / 2, population_by_step[:, 0],  height=bar_width, label=f"Initial ({initial_year})")
bars2 = ax2.barh(y_pos + bar_width / 2, population_by_step[:, -1], height=bar_width, label=f"Final ({initial_year + simulation_years})")

ax2.set_yticks(y_pos)
ax2.set_yticklabels(age_labels)
ax2.invert_yaxis()  # Youngest at top
ax2.set_xlabel("Population")
ax2.set_title("Initial vs Final Population by Age Group")
ax2.legend(loc="best")
ax2.grid(True, axis='x')

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/leslie_matrix_model.png", dpi=150)
plt.show()

print("Simulation complete.")
print(f"Initial total population : {int(total_population[0]):,}")
print(f"Final total population   : {int(total_population[-1]):,}")
print(f"Change                   : {int(total_population[-1] - total_population[0]):+,}")