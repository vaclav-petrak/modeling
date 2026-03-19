"""
Generate presentation images for Lesson 3 · Section 2: Agent-Based SIR.

Produces PDF figures in ../images/:
  - abm_transmission_decay.pdf   — exponential decay of infection probability
  - abm_infection_radius.pdf     — epidemic curves for different r_infect
  - abm_spatial_snapshots.pdf    — spatial snapshots at four time points
  - abm_random_walk.pdf          — single agent random walk trace
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
STATE_S, STATE_I, STATE_R = 1, 2, 3
C_S, C_I, C_R = "#2ca02c", "#d62728", "#1f77b4"


# ---------------------------------------------------------------------------
# Core model functions (matching the project notebook)
# ---------------------------------------------------------------------------
def update_position(x, y, area, rng):
    d = rng.randint(1, 4)
    if d == 1 and y < area:
        y += 1
    elif d == 2 and y > 0:
        y -= 1
    elif d == 3 and x > 0:
        x -= 1
    elif d == 4 and x < area:
        x += 1
    return x, y


def compute_infection_probability(idx, positions, states, p_infect, r_infect):
    if states[idx] != STATE_S:
        return 0.0
    dx = positions[:, 0].astype(float) - positions[idx, 0]
    dy = positions[:, 1].astype(float) - positions[idx, 1]
    dist = np.sqrt(dx**2 + dy**2)
    mask = (states == STATE_I) & (np.arange(len(states)) != idx) & (dist <= r_infect)
    if not np.any(mask):
        return 0.0
    probs = p_infect * np.exp(-dist[mask] / r_infect)
    return 1.0 - np.prod(1.0 - probs)


def update_health(state, prob, p_recover, rng):
    if state == STATE_S and prob > 0:
        if rng.random() < prob:
            return STATE_I
    elif state == STATE_I:
        if rng.random() < p_recover:
            return STATE_R
    return state


def simulate(area=40, population=200, initially_infected=5,
             steps=200, p_infect=0.25, p_recover=0.05,
             r_infect=3.0, seed=42):
    rng = random.Random(seed)
    positions = np.array([[rng.randint(0, area), rng.randint(0, area)]
                          for _ in range(population)], dtype=int)
    states = np.full(population, STATE_S, dtype=int)
    states[:initially_infected] = STATE_I
    s_h, i_h, r_h, pos_h, st_h = [], [], [], [], []
    for _ in range(steps):
        s_h.append(int(np.sum(states == STATE_S)))
        i_h.append(int(np.sum(states == STATE_I)))
        r_h.append(int(np.sum(states == STATE_R)))
        pos_h.append(positions.copy())
        st_h.append(states.copy())
        new = states.copy()
        for p in range(population):
            prob = compute_infection_probability(p, positions, states, p_infect, r_infect)
            new[p] = update_health(states[p], prob, p_recover, rng)
        states = new
        for p in range(population):
            x, y = update_position(int(positions[p, 0]), int(positions[p, 1]), area, rng)
            positions[p] = [x, y]
    return dict(susceptible=np.array(s_h), infected=np.array(i_h),
                recovered=np.array(r_h), positions=pos_h, states=st_h, area=area)


# ===================================================================
# Figure 1 — Transmission probability decay with distance
# ===================================================================
def fig_transmission_decay():
    d = np.linspace(0, 8, 200)
    fig, ax = plt.subplots(figsize=(7, 4))
    for r in [1.0, 2.0, 3.0, 5.0]:
        p = 0.25 * np.exp(-d / r)
        ax.plot(d, p, lw=2.5, label=f"$r_{{\\mathrm{{infect}}}} = {r:.0f}$")
    ax.set_xlabel("Distance $d$ to infected agent")
    ax.set_ylabel("Transmission probability $p_i$")
    ax.set_title("Exponential Decay of Infection Probability", fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_ylim(bottom=0)
    fig.savefig(OUT / "abm_transmission_decay.pdf")
    fig.savefig(OUT / "abm_transmission_decay.png")
    plt.close(fig)
    print("  ✓ abm_transmission_decay")


# ===================================================================
# Figure 2 — Effect of infection radius on epidemic curves
# ===================================================================
def fig_infection_radius():
    fig, ax = plt.subplots(figsize=(7, 4))
    for r in [1.0, 2.0, 3.0, 5.0]:
        res = simulate(r_infect=r, seed=42)
        ax.plot(res["infected"], lw=2.5, label=f"$r_{{\\mathrm{{infect}}}} = {r:.0f}$")
    ax.set_xlabel("Time step")
    ax.set_ylabel("Infected agents")
    ax.set_title("Effect of Infection Radius on Epidemic", fontweight="bold")
    ax.legend(fontsize=10)
    fig.savefig(OUT / "abm_infection_radius.pdf")
    fig.savefig(OUT / "abm_infection_radius.png")
    plt.close(fig)
    print("  ✓ abm_infection_radius")


# ===================================================================
# Figure 3 — Spatial snapshots at four time points
# ===================================================================
def fig_spatial_snapshots():
    res = simulate(seed=42)
    steps = [0, 30, 80, 150]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, t in zip(axes, steps):
        pos = res["positions"][t]
        st = res["states"][t]
        for state, c, lbl in [(STATE_S, C_S, "S"), (STATE_I, C_I, "I"), (STATE_R, C_R, "R")]:
            m = st == state
            ax.scatter(pos[m, 0], pos[m, 1], c=c, s=12, alpha=0.7, label=lbl)
        nI = int(np.sum(st == STATE_I))
        ax.set_title(f"$t = {t}$,  $I = {nI}$", fontsize=11)
        ax.set_xlim(0, res["area"])
        ax.set_ylim(0, res["area"])
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    axes[0].legend(loc="upper left", fontsize=8, markerscale=1.5)
    fig.suptitle("Spatial Spread of Infection Over Time", fontweight="bold", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "abm_spatial_snapshots.pdf")
    fig.savefig(OUT / "abm_spatial_snapshots.png")
    plt.close(fig)
    print("  ✓ abm_spatial_snapshots")


# ===================================================================
# Figure 4 — Single agent random walk
# ===================================================================
def fig_random_walk():
    rng = random.Random(7)
    x, y = 20, 20
    xs, ys = [x], [y]
    for _ in range(300):
        x, y = update_position(x, y, 40, rng)
        xs.append(x)
        ys.append(y)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(xs, ys, lw=0.8, alpha=0.6, color="gray")
    ax.scatter(xs[0], ys[0], c="green", s=80, zorder=5, label="Start")
    ax.scatter(xs[-1], ys[-1], c="red", s=80, zorder=5, label="End")
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 40)
    ax.set_aspect("equal")
    ax.set_title("Single Agent Random Walk (300 steps)", fontweight="bold")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "abm_random_walk.pdf")
    fig.savefig(OUT / "abm_random_walk.png")
    plt.close(fig)
    print("  ✓ abm_random_walk")


# ===================================================================
# Figure 5 — Compound probability from multiple infected neighbours
# ===================================================================
def fig_compound_probability():
    n_neighbours = np.arange(1, 11)
    fig, ax = plt.subplots(figsize=(7, 4))
    for d_val in [0.5, 1.0, 2.0, 3.0]:
        p_single = 0.25 * np.exp(-d_val / 3.0)
        P_combined = 1.0 - (1.0 - p_single) ** n_neighbours
        ax.plot(n_neighbours, P_combined, "o-", lw=2, markersize=6,
                label=f"$d = {d_val}$")
    ax.set_xlabel("Number of infected neighbours")
    ax.set_ylabel("Combined infection probability $P$")
    ax.set_title("Multiple Exposures Compound Risk\n"
                 "$(r_{\\mathrm{infect}} = 3,\\; p_{\\mathrm{infect}} = 0.25)$",
                 fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(n_neighbours)
    fig.tight_layout()
    fig.savefig(OUT / "abm_compound_probability.pdf")
    fig.savefig(OUT / "abm_compound_probability.png")
    plt.close(fig)
    print("  ✓ abm_compound_probability")


# ===================================================================
if __name__ == "__main__":
    print("Generating ABM presentation images …")
    fig_transmission_decay()
    fig_infection_radius()
    fig_spatial_snapshots()
    fig_random_walk()
    fig_compound_probability()
    print("All images saved to", OUT)
