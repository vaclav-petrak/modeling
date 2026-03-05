import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import cdist

# ==========================================
# 1. PARAMETERS
# ==========================================
# Space
WORLD_SIZE = 100.0

# Initial Populations
INIT_PREY = 150
INIT_PRED = 30
MAX_PREY = 10000 # Safety cap to prevent memory overflow

# Prey Parameters
PREY_SPEED = 1.5
PREY_REPRO_RATE = 0.025 # Probability of reproducing per step

# Predator Parameters
PRED_SPEED = 2.0
PRED_EAT_RADIUS = 2.5
PRED_ENERGY_GAIN = 15
PRED_STARVE_RATE = 1.0
PRED_REPRO_ENERGY = 40 # Energy required to reproduce
PRED_REPRO_RATE = 0.03 # Probability of reproducing if energy is high

# Migration (Extinction Prevention)
MIG_PROB_PREY = 0.1  # 10% chance per step for a new prey to migrate in
MIG_PROB_PRED = 0.05 # 5% chance per step for a new predator to migrate in

# ==========================================
# 2. INITIALIZATION
# ==========================================
# Agents are stored in NumPy arrays for computational speed.
# prey_pos: shape (N, 2) [x, y]
# pred_pos: shape (M, 2) [x, y]
# pred_energy: shape (M,) [energy]

prey_pos = np.random.rand(INIT_PREY, 2) * WORLD_SIZE
pred_pos = np.random.rand(INIT_PRED, 2) * WORLD_SIZE
pred_energy = np.ones(INIT_PRED) * 20.0

# History for plotting
history_prey = []
history_pred = []
time_steps = []
current_step = 0

# ==========================================
# 3. PLOTTING SETUP
# ==========================================
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 6))

# Subplot 1: Spatial Map
ax1 = plt.subplot(1, 2, 1)
ax1.set_xlim(0, WORLD_SIZE)
ax1.set_ylim(0, WORLD_SIZE)
ax1.set_title("Instantaneous Positions", fontsize=14)
ax1.set_aspect('equal')
scatter_prey = ax1.scatter([], [], c='#00FFCC', s=10, label='Prey', alpha=0.8)
scatter_pred = ax1.scatter([], [], c='#FF3366', s=30, label='Predator', marker='x')
ax1.legend(loc="upper right")

# Subplot 2: Population Dynamics
ax2 = plt.subplot(1, 2, 2)
ax2.set_xlim(0, 500)
ax2.set_ylim(0, INIT_PREY * 2)
ax2.set_title("Population Dynamics", fontsize=14)
ax2.set_xlabel("Time Step")
ax2.set_ylabel("Number of Agents")
line_prey, = ax2.plot([], [], c='#00FFCC', lw=2, label='Prey')
line_pred, = ax2.plot([], [], c='#FF3366', lw=2, label='Predator')
ax2.legend(loc="upper left")

# ==========================================
# 4. SIMULATION STEP (THE ENGINE)
# ==========================================
def update(frame):
    global prey_pos, pred_pos, pred_energy, current_step
    
    # --- A. MOVEMENT ---
    # Random walk with periodic boundary conditions (torus)
    if len(prey_pos) > 0:
        prey_pos += np.random.randn(len(prey_pos), 2) * PREY_SPEED
        prey_pos %= WORLD_SIZE 
        
    if len(pred_pos) > 0:
        pred_pos += np.random.randn(len(pred_pos), 2) * PRED_SPEED
        pred_pos %= WORLD_SIZE
        pred_energy -= PRED_STARVE_RATE # Predators lose energy by moving

    # --- B. PREDATION ---
    if len(prey_pos) > 0 and len(pred_pos) > 0:
        # Calculate all distances between predators and prey at once
        dists = cdist(pred_pos, prey_pos)
        
        eaten_prey = set()
        for i in range(len(pred_pos)):
            # Find prey within eating radius
            close_prey = np.where(dists[i] < PRED_EAT_RADIUS)[0]
            for p_idx in close_prey:
                if p_idx not in eaten_prey:
                    eaten_prey.add(p_idx)
                    pred_energy[i] += PRED_ENERGY_GAIN
                    break # One predator eats one prey per step maximum
                    
        # Remove eaten prey
        if eaten_prey:
            prey_pos = np.delete(prey_pos, list(eaten_prey), axis=0)

    # --- C. PREDATOR STARVATION ---
    alive_preds = pred_energy > 0
    pred_pos = pred_pos[alive_preds]
    pred_energy = pred_energy[alive_preds]

    # --- D. REPRODUCTION ---
    # Prey reproduction
    if len(prey_pos) > 0 and len(prey_pos) < MAX_PREY:
        reproducing_prey = np.random.rand(len(prey_pos)) < PREY_REPRO_RATE
        new_prey = prey_pos[reproducing_prey] + np.random.randn(np.sum(reproducing_prey), 2)
        new_prey %= WORLD_SIZE
        if len(new_prey) > 0:
            prey_pos = np.vstack((prey_pos, new_prey))

    # Predator reproduction
    if len(pred_pos) > 0:
        ready_to_repro = pred_energy > PRED_REPRO_ENERGY
        repro_attempt = np.random.rand(len(pred_pos)) < PRED_REPRO_RATE
        successful_repro = ready_to_repro & repro_attempt
        
        new_preds = pred_pos[successful_repro] + np.random.randn(np.sum(successful_repro), 2)
        new_preds %= WORLD_SIZE
        if len(new_preds) > 0:
            pred_pos = np.vstack((pred_pos, new_preds))
            # Halve energy of parent and child
            pred_energy[successful_repro] /= 2
            pred_energy = np.concatenate((pred_energy, pred_energy[successful_repro]))

    # --- E. MIGRATION (ANTI-EXTINCTION) ---
    if len(prey_pos) == 0 or np.random.rand() < MIG_PROB_PREY:
        new_migrant = np.random.rand(1, 2) * WORLD_SIZE
        prey_pos = new_migrant if len(prey_pos) == 0 else np.vstack((prey_pos, new_migrant))
        
    if len(pred_pos) == 0 or np.random.rand() < MIG_PROB_PRED:
        new_migrant = np.random.rand(1, 2) * WORLD_SIZE
        pred_pos = new_migrant if len(pred_pos) == 0 else np.vstack((pred_pos, new_migrant))
        pred_energy = np.append(pred_energy, 20.0)

    # --- F. RECORD & UPDATE PLOTS ---
    current_step += 1
    time_steps.append(current_step)
    history_prey.append(len(prey_pos))
    history_pred.append(len(pred_pos))

    # Update scatter plots
    scatter_prey.set_offsets(prey_pos)
    scatter_pred.set_offsets(pred_pos)

    # Update line plots
    line_prey.set_data(time_steps, history_prey)
    line_pred.set_data(time_steps, history_pred)
    
    # Adjust dynamic axes
    if current_step > ax2.get_xlim()[1] * 0.9:
        ax2.set_xlim(0, current_step * 1.5)
    max_pop = max(max(history_prey), max(history_pred))
    if max_pop > ax2.get_ylim()[1] * 0.9:
        ax2.set_ylim(0, max_pop * 1.2)

    return scatter_prey, scatter_pred, line_prey, line_pred

# Run the animation
ani = animation.FuncAnimation(fig, update, interval=30, blit=False, save_count=100)
plt.tight_layout()
plt.show()