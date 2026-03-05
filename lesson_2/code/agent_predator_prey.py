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

# Phase diagram trail length
PHASE_TRAIL = 2000  # Number of recent steps to show in phase diagram

# ==========================================
# 2. INITIALIZATION
# ==========================================
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
fig = plt.figure(figsize=(18, 6))
fig.patch.set_facecolor('#0d0d1a')

# Subplot 1: Spatial Map
ax1 = plt.subplot(1, 3, 1)
ax1.set_facecolor('#0d0d1a')
ax1.set_xlim(0, WORLD_SIZE)
ax1.set_ylim(0, WORLD_SIZE)
ax1.set_title("Instantaneous Positions", fontsize=13, color='white', pad=10)
ax1.set_aspect('equal')
scatter_prey = ax1.scatter([], [], c='#00FFCC', s=10, label='Prey', alpha=0.8)
scatter_pred = ax1.scatter([], [], c='#FF3366', s=30, label='Predator', marker='x')
ax1.legend(loc="upper right", framealpha=0.3)
ax1.tick_params(colors='#888888')
for spine in ax1.spines.values():
    spine.set_edgecolor('#333355')

# Subplot 2: Population Dynamics (Time Series)
ax2 = plt.subplot(1, 3, 2)
ax2.set_facecolor('#0d0d1a')
ax2.set_xlim(0, 500)
ax2.set_ylim(0, INIT_PREY * 2)
ax2.set_title("Population Dynamics", fontsize=13, color='white', pad=10)
ax2.set_xlabel("Time Step", color='#aaaacc')
ax2.set_ylabel("Number of Agents", color='#aaaacc')
line_prey, = ax2.plot([], [], c='#00FFCC', lw=2, label='Prey')
line_pred, = ax2.plot([], [], c='#FF3366', lw=2, label='Predator')
ax2.legend(loc="upper left", framealpha=0.3)
ax2.tick_params(colors='#888888')
for spine in ax2.spines.values():
    spine.set_edgecolor('#333355')

# Subplot 3: Phase Diagram (Prey vs Predator)
ax3 = plt.subplot(1, 3, 3)
ax3.set_facecolor('#0d0d1a')
ax3.set_xlim(0, INIT_PREY * 2)
ax3.set_ylim(0, INIT_PRED * 4)
ax3.set_title("Phase Diagram", fontsize=13, color='white', pad=10)
ax3.set_xlabel("Prey Population", color='#aaaacc')
ax3.set_ylabel("Predator Population", color='#aaaacc')
ax3.tick_params(colors='#888888')
for spine in ax3.spines.values():
    spine.set_edgecolor('#333355')

# Phase trail: a fading line of recent (prey, pred) coordinates
phase_trail_line, = ax3.plot([], [], lw=1.2, alpha=0.6, c='#8877ff')
phase_dot, = ax3.plot([], [], 'o', ms=7, c='#ffffff', zorder=5)

# Colormap for the trail to give a "time gradient" feel
# We'll update it manually using a LineCollection
from matplotlib.collections import LineCollection

# Use a LineCollection for the fading phase trail
phase_collection = LineCollection([], cmap='cool', linewidth=1.5, alpha=0.85)
ax3.add_collection(phase_collection)
phase_dot, = ax3.plot([], [], 'o', ms=8, c='#ffffff', zorder=5,
                      markeredgecolor='#ccccff', markeredgewidth=1)

# Label showing current cycle info
phase_text = ax3.text(0.05, 0.95, '', transform=ax3.transAxes,
                      color='#aaaacc', fontsize=9, va='top')

plt.tight_layout(pad=2.0)

# ==========================================
# 4. SIMULATION STEP (THE ENGINE)
# ==========================================
def update(frame):
    global prey_pos, pred_pos, pred_energy, current_step
    
    # --- A. MOVEMENT ---
    if len(prey_pos) > 0:
        prey_pos += np.random.randn(len(prey_pos), 2) * PREY_SPEED
        prey_pos %= WORLD_SIZE 
        
    if len(pred_pos) > 0:
        pred_pos += np.random.randn(len(pred_pos), 2) * PRED_SPEED
        pred_pos %= WORLD_SIZE
        pred_energy -= PRED_STARVE_RATE

    # --- B. PREDATION ---
    if len(prey_pos) > 0 and len(pred_pos) > 0:
        dists = cdist(pred_pos, prey_pos)
        
        eaten_prey = set()
        for i in range(len(pred_pos)):
            close_prey = np.where(dists[i] < PRED_EAT_RADIUS)[0]
            for p_idx in close_prey:
                if p_idx not in eaten_prey:
                    eaten_prey.add(p_idx)
                    pred_energy[i] += PRED_ENERGY_GAIN
                    break
                    
        if eaten_prey:
            prey_pos = np.delete(prey_pos, list(eaten_prey), axis=0)

    # --- C. PREDATOR STARVATION ---
    alive_preds = pred_energy > 0
    pred_pos = pred_pos[alive_preds]
    pred_energy = pred_energy[alive_preds]

    # --- D. REPRODUCTION ---
    if len(prey_pos) > 0 and len(prey_pos) < MAX_PREY:
        reproducing_prey = np.random.rand(len(prey_pos)) < PREY_REPRO_RATE
        new_prey = prey_pos[reproducing_prey] + np.random.randn(np.sum(reproducing_prey), 2)
        new_prey %= WORLD_SIZE
        if len(new_prey) > 0:
            prey_pos = np.vstack((prey_pos, new_prey))

    if len(pred_pos) > 0:
        ready_to_repro = pred_energy > PRED_REPRO_ENERGY
        repro_attempt = np.random.rand(len(pred_pos)) < PRED_REPRO_RATE
        successful_repro = ready_to_repro & repro_attempt
        
        new_preds = pred_pos[successful_repro] + np.random.randn(np.sum(successful_repro), 2)
        new_preds %= WORLD_SIZE
        if len(new_preds) > 0:
            pred_pos = np.vstack((pred_pos, new_preds))
            pred_energy[successful_repro] /= 2
            pred_energy = np.concatenate((pred_energy, pred_energy[successful_repro]))

    # --- E. MIGRATION ---
    if len(prey_pos) == 0 or np.random.rand() < MIG_PROB_PREY:
        new_migrant = np.random.rand(1, 2) * WORLD_SIZE
        prey_pos = new_migrant if len(prey_pos) == 0 else np.vstack((prey_pos, new_migrant))
        
    if len(pred_pos) == 0 or np.random.rand() < MIG_PROB_PRED:
        new_migrant = np.random.rand(1, 2) * WORLD_SIZE
        pred_pos = new_migrant if len(pred_pos) == 0 else np.vstack((pred_pos, new_migrant))
        pred_energy = np.append(pred_energy, 20.0)

    # --- F. RECORD & UPDATE PLOTS ---
    current_step += 1
    n_prey = len(prey_pos)
    n_pred = len(pred_pos)
    time_steps.append(current_step)
    history_prey.append(n_prey)
    history_pred.append(n_pred)

    # -- Subplot 1: Scatter --
    scatter_prey.set_offsets(prey_pos)
    scatter_pred.set_offsets(pred_pos)

    # -- Subplot 2: Time series --
    line_prey.set_data(time_steps, history_prey)
    line_pred.set_data(time_steps, history_pred)
    
    if current_step > ax2.get_xlim()[1] * 0.9:
        ax2.set_xlim(0, current_step * 1.5)
    max_pop = max(max(history_prey), max(history_pred))
    if max_pop > ax2.get_ylim()[1] * 0.9:
        ax2.set_ylim(0, max_pop * 1.2)

    # -- Subplot 3: Phase diagram --
    # Take the last PHASE_TRAIL steps
    trail_prey = history_prey[-PHASE_TRAIL:]
    trail_pred = history_pred[-PHASE_TRAIL:]

    if len(trail_prey) >= 2:
        # Build segments for LineCollection
        points = np.array([trail_prey, trail_pred]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Color values 0→1 representing old→new
        colors = np.linspace(0, 1, len(segments))
        phase_collection.set_segments(segments)
        phase_collection.set_array(colors)
        phase_collection.set_clim(0, 1)

    # Current position dot
    phase_dot.set_data([n_prey], [n_pred])

    # Auto-scale phase axes
    if history_prey:
        max_prey_all = max(history_prey)
        max_pred_all = max(history_pred)
        ax3.set_xlim(0, max(max_prey_all * 1.15, 10))
        ax3.set_ylim(0, max(max_pred_all * 1.15, 5))

    phase_text.set_text(f"Prey: {n_prey}  |  Pred: {n_pred}\nStep: {current_step}")

    return scatter_prey, scatter_pred, line_prey, line_pred, phase_collection, phase_dot, phase_text

# Run the animation
ani = animation.FuncAnimation(fig, update, interval=30, blit=False, save_count=100)
plt.tight_layout(pad=2.0)
plt.show()