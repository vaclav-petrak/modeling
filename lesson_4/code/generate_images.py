"""
Generate all images for Lesson 4 presentation.
Run from the lesson_4 directory:
    python code/generate_images.py

Images are saved to lesson_4/images/
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os

IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')
os.makedirs(IMG, exist_ok=True)

plt.rcParams.update({
    'figure.dpi': 200,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.size': 12,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

# ── Color palette (matches existing code) ─────────────────────────────────
GROUND = np.array([76, 66, 70]) / 255
TREES  = np.array([118, 176, 65]) / 255
FIRE   = np.array([228, 87, 46]) / 255
forest_cmap = ListedColormap([GROUND, TREES, FIRE])

# ============================================================
# 1. FOREST FIRE — single simulation snapshot + time series
# ============================================================
def detect_fire(row, col, grid):
    h, w = grid.shape
    neighbourhood = grid[max(0, row-1):min(h, row+2), max(0, col-1):min(w, col+2)]
    return int(np.max(neighbourhood) == 2)

def update_cell(state, fire_nearby, p_plant, p_ign):
    if state == 0:
        return 1 if np.random.random() < p_plant else 0
    if state == 1:
        return 2 if (fire_nearby or np.random.random() < p_ign) else 1
    return 0  # burning -> empty

def run_forest_fire(area, iterations, p_plant, p_ign, seed=42):
    np.random.seed(seed)
    grid = np.zeros((area, area), dtype=int)
    tree_hist = np.zeros(iterations)
    fire_hist = np.zeros(iterations)
    snapshots = {}
    for t in range(iterations):
        new_grid = np.zeros_like(grid)
        for r in range(area):
            for c in range(area):
                fn = detect_fire(r, c, grid)
                new_grid[r, c] = update_cell(int(grid[r, c]), fn, p_plant, p_ign)
        grid = new_grid
        tree_hist[t] = np.sum(grid == 1)
        fire_hist[t] = np.sum(grid == 2)
        if t in (100, 200, 400):
            snapshots[t] = grid.copy()
    return grid, tree_hist, fire_hist, snapshots

print('Generating forest fire simulation...')
grid_ff, trees_ff, fire_ff, snaps_ff = run_forest_fire(100, 500, 0.004, 0.00002)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.imshow(grid_ff, cmap=forest_cmap, vmin=0, vmax=2)
ax1.set_title('Forest at $t = 500$', fontweight='bold')
ax1.axis('off')
ax2.plot(trees_ff, lw=1.5, color=TREES, label='Trees')
ax2.plot(fire_ff * 10, lw=1.5, color=FIRE, label='Fire ($\\times 10$)')
ax2.set_xlabel('Time step')
ax2.set_ylabel('Count')
ax2.set_title('Population over time', fontweight='bold')
ax2.legend()
ax2.set_xlim(0, 500)
plt.tight_layout()
fig.savefig(f'{IMG}/forest_fire_simulation.pdf')
fig.savefig(f'{IMG}/forest_fire_simulation.png')
plt.close(fig)
print('  forest_fire_simulation done')

# ── Forest fire — parameter comparison ──
print('Generating forest fire parameter comparison...')
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
params = [
    (0.002, 0.0001, 'Slow growth, frequent fire'),
    (0.004, 0.00002, 'Balanced (default)'),
    (0.01, 0.000005, 'Fast growth, rare fire'),
]
for ax, (pp, pi, title) in zip(axes, params):
    g, th, fh, _ = run_forest_fire(80, 400, pp, pi, seed=7)
    ax.imshow(g, cmap=forest_cmap, vmin=0, vmax=2)
    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.axis('off')
fig.suptitle('Effect of $p_{\\mathrm{plant}}$ and $p_{\\mathrm{ignition}}$', fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/forest_fire_parameters.pdf')
fig.savefig(f'{IMG}/forest_fire_parameters.png')
plt.close(fig)
print('  forest_fire_parameters done')

# ============================================================
# 2. GAME OF LIFE — snapshots
# ============================================================
def gol_step(grid):
    h, w = grid.shape
    new = np.zeros_like(grid)
    for r in range(h):
        for c in range(w):
            nbrs = int(np.sum(grid[max(0,r-1):min(h,r+2), max(0,c-1):min(w,c+2)])) - int(grid[r,c])
            if grid[r,c] == 1:
                new[r,c] = 1 if nbrs in (2,3) else 0
            else:
                new[r,c] = 1 if nbrs == 3 else 0
    return new

print('Generating Game of Life snapshots...')
# Glider gun (Gosper)
gun = np.zeros((40, 50), dtype=int)
gun_cells = [
    (5,1),(5,2),(6,1),(6,2),
    (3,13),(3,14),(4,12),(4,16),(5,11),(5,17),(6,11),(6,15),(6,17),(6,18),
    (7,11),(7,17),(8,12),(8,16),(9,13),(9,14),
    (1,25),(2,23),(2,25),(3,21),(3,22),(4,21),(4,22),(5,21),(5,22),
    (6,23),(6,25),(7,25),
    (3,35),(3,36),(4,35),(4,36),
]
for r,c in gun_cells:
    gun[r,c] = 1

dead_c = np.array([238, 243, 106]) / 255
live_c = np.array([63, 48, 71]) / 255
gol_cmap = ListedColormap([dead_c, live_c])

frames = [gun.copy()]
g = gun.copy()
for i in range(120):
    g = gol_step(g)
    if i in (29, 59, 89, 119):
        frames.append(g.copy())

fig, axes = plt.subplots(1, 5, figsize=(16, 3))
labels = ['$t = 0$', '$t = 30$', '$t = 60$', '$t = 90$', '$t = 120$']
for ax, frame, lab in zip(axes, frames, labels):
    ax.imshow(frame, cmap=gol_cmap, vmin=0, vmax=1)
    ax.set_title(lab, fontweight='bold')
    ax.axis('off')
fig.suptitle("Conway's Game of Life — Gosper Glider Gun", fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/gol_glider_gun.pdf')
fig.savefig(f'{IMG}/gol_glider_gun.png')
plt.close(fig)
print('  gol_glider_gun done')

# ============================================================
# 3. ELEMENTARY CELLULAR AUTOMATA
# ============================================================
def rule_to_table(rule_number):
    return {((i >> 2) & 1, (i >> 1) & 1, i & 1): (rule_number >> i) & 1 for i in range(8)}

def run_eca(rule_number, width=201, steps=100):
    table = rule_to_table(rule_number)
    grid = np.zeros((steps, width), dtype=int)
    grid[0, width // 2] = 1
    for t in range(1, steps):
        for i in range(width):
            left = grid[t-1, (i-1) % width]
            center = grid[t-1, i]
            right = grid[t-1, (i+1) % width]
            grid[t, i] = table[(left, center, right)]
    return grid

# Gallery of rules
print('Generating ECA gallery...')
rules_gallery = [30, 90, 110, 184, 54, 150]
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
for ax, rn in zip(axes.flat, rules_gallery):
    g = run_eca(rn, 201, 100)
    ax.imshow(g, cmap='binary', interpolation='nearest')
    ax.set_title(f'Rule {rn}', fontweight='bold', fontsize=13)
    ax.axis('off')
fig.suptitle('Elementary Cellular Automata — Gallery', fontweight='bold', fontsize=15)
plt.tight_layout()
fig.savefig(f'{IMG}/eca_gallery.pdf')
fig.savefig(f'{IMG}/eca_gallery.png')
plt.close(fig)
print('  eca_gallery done')

# Individual large rules
for rn in (30, 90, 110):
    g = run_eca(rn, 401, 200)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(g, cmap='binary', interpolation='nearest', aspect='auto')
    ax.set_title(f'Rule {rn}', fontweight='bold', fontsize=14)
    ax.set_xlabel('Cell')
    ax.set_ylabel('Time step')
    fig.savefig(f'{IMG}/eca_rule{rn}.pdf')
    fig.savefig(f'{IMG}/eca_rule{rn}.png')
    plt.close(fig)
    print(f'  eca_rule{rn} done')

# Rule lookup visualization for Rule 110
print('Generating Rule 110 lookup table...')
table_110 = rule_to_table(110)
fig, axes = plt.subplots(1, 8, figsize=(14, 2))
for idx, ax in enumerate(axes):
    pattern = ((idx >> 2) & 1, (idx >> 1) & 1, idx & 1)
    output = table_110[pattern]
    # Draw 3 cells on top
    for j, v in enumerate(pattern):
        rect = plt.Rectangle((j, 1), 1, 1, facecolor='black' if v else 'white', edgecolor='gray', lw=2)
        ax.add_patch(rect)
    # Draw output cell below centre
    rect = plt.Rectangle((1, 0), 1, 1, facecolor='black' if output else 'white', edgecolor='gray', lw=2)
    ax.add_patch(rect)
    ax.set_xlim(-0.1, 3.1)
    ax.set_ylim(-0.3, 2.3)
    ax.set_aspect('equal')
    ax.axis('off')
fig.suptitle('Rule 110 — Lookup Table', fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/eca_rule110_table.pdf')
fig.savefig(f'{IMG}/eca_rule110_table.png')
plt.close(fig)
print('  eca_rule110_table done')

# ============================================================
# 4. WOLFRAM CLASSES illustration
# ============================================================
print('Generating Wolfram classes...')
class_rules = [(0, 'Class I — Rule 0'), (4, 'Class II — Rule 4'), (30, 'Class III — Rule 30'), (110, 'Class IV — Rule 110')]
fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
for ax, (rn, title) in zip(axes, class_rules):
    g = run_eca(rn, 201, 100)
    ax.imshow(g, cmap='binary', interpolation='nearest')
    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.axis('off')
fig.suptitle("Wolfram's Four Classes of CA Behaviour", fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/eca_wolfram_classes.pdf')
fig.savefig(f'{IMG}/eca_wolfram_classes.png')
plt.close(fig)
print('  eca_wolfram_classes done')

print('\n=== All lesson 4 images generated ===')
