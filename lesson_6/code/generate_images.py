#!/usr/bin/env python3
"""Generate figures for Lesson 6 — Synthesis & Model Comparison."""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "images"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
    "font.family": "serif",
})

BLUE = "#247BA0"
RED = "#F25F5C"
GREEN = "#2EAA60"
GRAY = "#50514F"
ORANGE = "#F28C28"


# =============================================================================
# Figure 1: Model Taxonomy — Axes of Modelling Approaches
# =============================================================================
def fig_model_taxonomy():
    fig, ax = plt.subplots(figsize=(8, 6))

    models = {
        "Malthusian\nGrowth":       (0.15, 0.15),
        "Logistic\nGrowth":         (0.25, 0.20),
        "Lotka-\nVolterra":         (0.35, 0.30),
        "SIR ODE":                  (0.40, 0.40),
        "SEIR ODE":                 (0.50, 0.45),
        "Leslie\nMatrix":           (0.30, 0.50),
        "Logistic\nMap":            (0.55, 0.25),
        "Elementary\nCA":           (0.65, 0.55),
        "Game of\nLife":            (0.70, 0.60),
        "Forest\nFire CA":          (0.75, 0.70),
        "NaSch\nTraffic":           (0.80, 0.65),
        "ABM\nEpidemic":            (0.85, 0.80),
        "ABM\nPredator-Prey":       (0.90, 0.85),
        "DLA":                      (0.72, 0.50),
        "Stochastic\nLogistic":     (0.45, 0.60),
    }

    colors_map = {
        "Malthusian\nGrowth": BLUE, "Logistic\nGrowth": BLUE,
        "Lotka-\nVolterra": BLUE, "SIR ODE": BLUE, "SEIR ODE": BLUE,
        "Leslie\nMatrix": BLUE, "Stochastic\nLogistic": ORANGE,
        "Logistic\nMap": RED,
        "Elementary\nCA": GREEN, "Game of\nLife": GREEN,
        "Forest\nFire CA": GREEN, "NaSch\nTraffic": GREEN,
        "ABM\nEpidemic": ORANGE, "ABM\nPredator-Prey": ORANGE,
        "DLA": GREEN,
    }

    for name, (x, y) in models.items():
        c = colors_map.get(name, GRAY)
        ax.scatter(x, y, s=120, color=c, zorder=3, edgecolors="white", linewidths=0.5)
        ax.annotate(name, (x, y), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=7, color=GRAY)

    # Legend patches
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=BLUE, label="Equation-based (ODE/matrix)"),
        Patch(facecolor=GREEN, label="Cellular automata"),
        Patch(facecolor=ORANGE, label="Agent-based / stochastic"),
        Patch(facecolor=RED, label="Discrete maps (chaos)"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=8,
              framealpha=0.9, edgecolor=GRAY)

    ax.set_xlabel("Spatial explicitness  →", fontsize=11, fontweight="bold")
    ax.set_ylabel("Agent heterogeneity / stochasticity  →", fontsize=11, fontweight="bold")
    ax.set_xlim(0.05, 1.0)
    ax.set_ylim(0.05, 1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Model Taxonomy: Course Landscape", fontweight="bold", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "model_taxonomy.pdf", bbox_inches="tight")
    fig.savefig(OUT / "model_taxonomy.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ model_taxonomy")


# =============================================================================
# Figure 2: ODE vs ABM comparison — SIR epidemic curves
# =============================================================================
def fig_ode_vs_abm():
    # --- ODE SIR ---
    dt = 0.1
    T = 100
    t = np.arange(0, T, dt)
    N = 1000
    beta, gamma = 0.3, 0.1
    S, I, R = np.zeros_like(t), np.zeros_like(t), np.zeros_like(t)
    S[0], I[0], R[0] = 990/N, 10/N, 0
    for i in range(len(t)-1):
        dS = -beta * S[i] * I[i]
        dI = beta * S[i] * I[i] - gamma * I[i]
        dR = gamma * I[i]
        S[i+1] = S[i] + dS * dt
        I[i+1] = I[i] + dI * dt
        R[i+1] = R[i] + dR * dt

    # --- ABM SIR (simplified stochastic) ---
    rng = np.random.default_rng(42)
    n_runs = 5
    abm_I = []
    for run in range(n_runs):
        states = np.zeros(N, dtype=int)  # 0=S, 1=I, 2=R
        states[rng.choice(N, 10, replace=False)] = 1
        I_hist = []
        for step in range(int(T/dt)):
            n_infected = np.sum(states == 1)
            n_susceptible = np.sum(states == 0)
            I_hist.append(n_infected / N)
            if n_infected == 0:
                I_hist.extend([0] * (int(T/dt) - step - 1))
                break
            # Infection: each S has prob beta*I/N per step
            p_infect = 1 - (1 - beta * dt) ** (n_infected)
            s_mask = states == 0
            new_infections = rng.random(N) < p_infect
            states[s_mask & new_infections] = 1
            # Recovery
            i_mask = states == 1
            recoveries = rng.random(N) < gamma * dt
            states[i_mask & recoveries] = 2
        abm_I.append(np.array(I_hist[:len(t)]))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)

    ax1.plot(t, S, color=GREEN, lw=2, label="S")
    ax1.plot(t, I, color=RED, lw=2, label="I")
    ax1.plot(t, R, color=GRAY, lw=2, label="R")
    ax1.set_title("ODE Model (deterministic)", fontweight="bold")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Fraction of population")
    ax1.legend(fontsize=9)

    for i, run_I in enumerate(abm_I):
        if len(run_I) == len(t):
            ax2.plot(t, run_I, color=RED, alpha=0.4, lw=1,
                     label="ABM runs" if i == 0 else None)
    ax2.plot(t, I, color=RED, lw=2, ls="--", label="ODE (reference)")
    ax2.set_title("ABM Model (stochastic runs)", fontweight="bold")
    ax2.set_xlabel("Time")
    ax2.legend(fontsize=9)

    fig.suptitle("Equation-Based vs Agent-Based: SIR Epidemic",
                 fontweight="bold", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "ode_vs_abm_sir.pdf", bbox_inches="tight")
    fig.savefig(OUT / "ode_vs_abm_sir.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ ode_vs_abm_sir")


# =============================================================================
# Figure 3: Sensitivity analysis — tornado diagram
# =============================================================================
def fig_sensitivity_tornado():
    params = ["$\\beta$ (transmission)", "$\\gamma$ (recovery)",
              "$N_0$ (initial pop.)", "$I_0$ (initial infected)",
              "$\\sigma$ (noise)"]
    low = [-35, 15, -5, -20, -8]
    high = [40, -12, 8, 25, 12]

    fig, ax = plt.subplots(figsize=(8, 4))
    y_pos = np.arange(len(params))

    ax.barh(y_pos, high, height=0.5, color=RED, alpha=0.8, label="High value")
    ax.barh(y_pos, low, height=0.5, color=BLUE, alpha=0.8, label="Low value")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params)
    ax.set_xlabel("% Change in peak infected")
    ax.axvline(0, color="black", lw=0.8)
    ax.set_title("Tornado Diagram: Parameter Sensitivity of SIR Peak",
                 fontweight="bold", fontsize=12)
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "sensitivity_tornado.pdf", bbox_inches="tight")
    fig.savefig(OUT / "sensitivity_tornado.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ sensitivity_tornado")


# =============================================================================
# Figure 4: Convergence — Euler step size comparison
# =============================================================================
def fig_euler_convergence():
    def logistic_exact(t, r=0.5, K=100, N0=5):
        return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

    def euler_logistic(dt, T=40, r=0.5, K=100, N0=5):
        steps = int(T / dt)
        t = np.linspace(0, T, steps + 1)
        N = np.zeros(steps + 1)
        N[0] = N0
        for i in range(steps):
            N[i+1] = N[i] + dt * r * N[i] * (1 - N[i] / K)
        return t, N

    t_exact = np.linspace(0, 40, 500)
    N_exact = logistic_exact(t_exact)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    dts = [0.5, 2.0, 5.0, 8.0]
    colors = [GREEN, BLUE, ORANGE, RED]
    errors = []

    for dt_val, c in zip(dts, colors):
        t_e, N_e = euler_logistic(dt_val)
        ax1.plot(t_e, N_e, color=c, lw=1.5, label=f"dt = {dt_val}")
        # Compute max error
        N_ref = logistic_exact(t_e)
        errors.append(np.max(np.abs(N_e - N_ref)))

    ax1.plot(t_exact, N_exact, "k--", lw=2, label="Exact solution")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population N(t)")
    ax1.set_title("Euler Method: Step Size Effect", fontweight="bold")
    ax1.legend(fontsize=8)

    ax2.loglog(dts, errors, "o-", color=BLUE, lw=2, markersize=8)
    ax2.set_xlabel("Step size $\\Delta t$")
    ax2.set_ylabel("Maximum absolute error")
    ax2.set_title("Convergence: Error vs Step Size", fontweight="bold")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT / "euler_convergence.pdf", bbox_inches="tight")
    fig.savefig(OUT / "euler_convergence.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ euler_convergence")


# =============================================================================
# Figure 5: Decision flowchart — text-based (rendered as table/diagram)
# =============================================================================
def fig_decision_flowchart():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    box_style = dict(boxstyle="round,pad=0.5", facecolor="white",
                     edgecolor=BLUE, linewidth=2)
    leaf_style_ode = dict(boxstyle="round,pad=0.4", facecolor="#E3F2FD",
                          edgecolor=BLUE, linewidth=1.5)
    leaf_style_ca = dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9",
                         edgecolor=GREEN, linewidth=1.5)
    leaf_style_abm = dict(boxstyle="round,pad=0.4", facecolor="#FFF3E0",
                          edgecolor=ORANGE, linewidth=1.5)
    q_style = dict(boxstyle="round,pad=0.5", facecolor="#FFF9C4",
                   edgecolor=ORANGE, linewidth=2)

    # Root question
    ax.text(5, 6.2, "Is spatial structure\nimportant?",
            ha="center", va="center", fontsize=11, fontweight="bold",
            bbox=q_style)

    # Left branch: No spatial
    ax.annotate("", xy=(2.5, 5.0), xytext=(4.0, 5.7),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))
    ax.text(3.2, 5.5, "No", fontsize=9, color=GRAY, fontweight="bold")

    ax.text(2.5, 4.7, "Are individuals\nidentical?",
            ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=q_style)

    ax.annotate("", xy=(1.2, 3.5), xytext=(1.8, 4.2),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))
    ax.text(1.0, 4.0, "Yes", fontsize=9, color=GRAY, fontweight="bold")
    ax.text(1.2, 3.2, "ODE / Difference\nEquation",
            ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=leaf_style_ode)

    ax.annotate("", xy=(3.8, 3.5), xytext=(3.2, 4.2),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))
    ax.text(3.9, 4.0, "No", fontsize=9, color=GRAY, fontweight="bold")
    ax.text(3.8, 3.2, "Leslie Matrix /\nAge-Structured",
            ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=leaf_style_ode)

    # Right branch: Spatial
    ax.annotate("", xy=(7.5, 5.0), xytext=(6.0, 5.7),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))
    ax.text(6.8, 5.5, "Yes", fontsize=9, color=GRAY, fontweight="bold")

    ax.text(7.5, 4.7, "Are agents\nautonomous?",
            ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=q_style)

    ax.annotate("", xy=(6.2, 3.5), xytext=(6.8, 4.2),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))
    ax.text(5.9, 4.0, "No", fontsize=9, color=GRAY, fontweight="bold")
    ax.text(6.2, 3.2, "Cellular\nAutomaton",
            ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=leaf_style_ca)

    ax.annotate("", xy=(8.8, 3.5), xytext=(8.2, 4.2),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))
    ax.text(8.9, 4.0, "Yes", fontsize=9, color=GRAY, fontweight="bold")
    ax.text(8.8, 3.2, "Agent-Based\nModel",
            ha="center", va="center", fontsize=10, fontweight="bold",
            bbox=leaf_style_abm)

    # Examples
    ax.text(1.2, 2.3, "SIR, Logistic,\nLotka-Volterra",
            ha="center", va="center", fontsize=8, color=GRAY, style="italic")
    ax.text(3.8, 2.3, "Leslie Matrix,\nStage-structured",
            ha="center", va="center", fontsize=8, color=GRAY, style="italic")
    ax.text(6.2, 2.3, "Forest Fire,\nGame of Life,\nTraffic NaSch",
            ha="center", va="center", fontsize=8, color=GRAY, style="italic")
    ax.text(8.8, 2.3, "ABM Epidemic,\nPredator-Prey ABM,\nDLA",
            ha="center", va="center", fontsize=8, color=GRAY, style="italic")

    # Stochasticity note
    ax.text(5, 1.0, "↕  Add stochasticity to any approach: noise terms (SDE), "
            "random events (CA), random agent decisions (ABM)",
            ha="center", va="center", fontsize=9, color=ORANGE,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF3E0",
                      edgecolor=ORANGE, linewidth=1, alpha=0.7))

    ax.set_title("Choosing a Modelling Approach", fontweight="bold", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "decision_flowchart.pdf", bbox_inches="tight")
    fig.savefig(OUT / "decision_flowchart.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ decision_flowchart")


# =============================================================================
# Figure 6: Good vs Bad visualisation
# =============================================================================
def fig_good_vs_bad_viz():
    t = np.linspace(0, 50, 200)
    S = 0.99 * np.exp(-0.05 * t)
    I = 0.6 * (np.exp(-0.05 * t) - np.exp(-0.15 * t))
    R = 1 - S - np.maximum(I, 0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Bad: no labels, no legend, rainbow, thick grid
    ax1.plot(t, S, color="cyan", lw=1)
    ax1.plot(t, I, color="magenta", lw=1)
    ax1.plot(t, R, color="yellow", lw=1)
    ax1.set_facecolor("#f0f0f0")
    ax1.grid(True, color="white", lw=2)
    ax1.set_title("Unlabelled, poor colours", fontweight="bold", fontsize=11,
                  color=RED)
    # Deliberately add no labels or legend
    ax1.spines["top"].set_visible(True)
    ax1.spines["right"].set_visible(True)

    # Good: proper labels, legend, clean style
    ax2.plot(t, S, color=GREEN, lw=2, label="Susceptible")
    ax2.plot(t, I, color=RED, lw=2, label="Infected")
    ax2.plot(t, R, color=GRAY, lw=2, label="Recovered")
    ax2.set_xlabel("Time (days)")
    ax2.set_ylabel("Fraction of population")
    ax2.set_title("Labelled, accessible colours", fontweight="bold",
                  fontsize=11, color=GREEN)
    ax2.legend(fontsize=9)

    fig.suptitle("Visualisation: Before & After", fontweight="bold",
                 fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "good_vs_bad_viz.pdf", bbox_inches="tight")
    fig.savefig(OUT / "good_vs_bad_viz.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ good_vs_bad_viz")


# =============================================================================
# Figure 7: Course map — connections between lessons
# =============================================================================
def fig_course_map():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1, 3.5)
    ax.axis("off")

    lessons = [
        (0, 2, "L1\nDiscrete\nDynamics", BLUE),
        (1, 2, "L2\nSystem\nDynamics", BLUE),
        (2, 2, "L3\nEpidemiology\n& Agents", ORANGE),
        (3, 2, "L4\nCellular\nAutomata", GREEN),
        (4, 2, "L5\nChaos &\nFractals", RED),
        (5, 2, "L6\nSynthesis", GRAY),
    ]

    for x, y, label, color in lessons:
        ax.add_patch(plt.Circle((x, y), 0.42, color=color, alpha=0.15, zorder=1))
        ax.add_patch(plt.Circle((x, y), 0.42, fill=False, edgecolor=color,
                                lw=2, zorder=2))
        ax.text(x, y, label, ha="center", va="center", fontsize=8,
                fontweight="bold", color=color, zorder=3)

    # Arrows between consecutive lessons
    for i in range(5):
        ax.annotate("", xy=(i + 0.55, 2), xytext=(i + 0.45, 2),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=GRAY))

    # Cross-connections
    connections = [
        (0, 2, "logistic growth", 0.35),
        (0, 4, "logistic map", -0.7),
        (1, 2, "SIR ODE → ABM", 0.15),
        (1, 3, "spatial models", -0.5),
        (2, 3, "CA epidemics", 0.15),
        (3, 4, "emergence", -0.4),
    ]

    for src, dst, label, curve in connections:
        ax.annotate("",
                    xy=(dst, 2 - 0.45),
                    xytext=(src, 2 - 0.45),
                    arrowprops=dict(arrowstyle="->", lw=1, color=GRAY,
                                   alpha=0.5,
                                   connectionstyle=f"arc3,rad={curve}"))
        mid_x = (src + dst) / 2
        mid_y = 2 - 0.45 + curve * 1.2
        ax.text(mid_x, mid_y, label, ha="center", va="center",
                fontsize=6.5, color=GRAY, style="italic", alpha=0.8)

    ax.set_title("Course Concept Map", fontweight="bold", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "course_map.pdf", bbox_inches="tight")
    fig.savefig(OUT / "course_map.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ course_map")


# =============================================================================
# Figure 8: Overfitting illustration
# =============================================================================
def fig_overfitting():
    rng = np.random.default_rng(12)
    t_data = np.linspace(0, 10, 12)
    y_true = 3 * np.sin(0.5 * t_data) + 10
    y_data = y_true + rng.normal(0, 1.2, len(t_data))

    t_smooth = np.linspace(0, 10, 300)
    y_true_smooth = 3 * np.sin(0.5 * t_smooth) + 10

    # Underfit: linear
    coeffs_1 = np.polyfit(t_data, y_data, 1)
    y_under = np.polyval(coeffs_1, t_smooth)

    # Good fit: degree 4
    coeffs_4 = np.polyfit(t_data, y_data, 4)
    y_good = np.polyval(coeffs_4, t_smooth)

    # Overfit: degree 11
    coeffs_11 = np.polyfit(t_data, y_data, 11)
    y_over = np.polyval(coeffs_11, t_smooth)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13, 4), sharey=True)

    for ax, y_fit, title, color in [
        (ax1, y_under, "Underfitting (linear)", BLUE),
        (ax2, y_good, "Good fit (degree 4)", GREEN),
        (ax3, y_over, "Overfitting (degree 11)", RED),
    ]:
        ax.scatter(t_data, y_data, color="black", s=40, zorder=3, label="Data")
        ax.plot(t_smooth, y_true_smooth, "k--", lw=1, alpha=0.4, label="True process")
        ax.plot(t_smooth, y_fit, color=color, lw=2, label="Model")
        ax.set_title(title, fontweight="bold", color=color, fontsize=11)
        ax.set_xlabel("Time")
        ax.legend(fontsize=7, loc="lower left")
        ax.set_ylim(3, 18)

    ax1.set_ylabel("Observed value")
    fig.suptitle("Model Complexity: Finding the Right Balance",
                 fontweight="bold", fontsize=13, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "overfitting.pdf", bbox_inches="tight")
    fig.savefig(OUT / "overfitting.png", bbox_inches="tight")
    plt.close(fig)
    print("✓ overfitting")


# =============================================================================
if __name__ == "__main__":
    fig_model_taxonomy()
    fig_ode_vs_abm()
    fig_sensitivity_tornado()
    fig_euler_convergence()
    fig_decision_flowchart()
    fig_good_vs_bad_viz()
    fig_course_map()
    fig_overfitting()
    print(f"\nAll figures saved to {OUT}")
