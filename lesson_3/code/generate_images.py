"""
Generate all images for Lesson 3 presentation.
Run from the lesson_3 directory:
    python code/generate_images.py

Images are saved to lesson_3/images/
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random as stdlib_random
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

# ── Colours ────────────────────────────────────────────────
C_S = '#2ecc71'   # green - susceptible
C_I = '#e74c3c'   # red   - infected
C_R = '#3498db'   # blue  - recovered
C_E = '#f39c12'   # orange - exposed

# ============================================================
# Helper: ODE SIR simulation (Euler)
# ============================================================
def sir_euler(S0, I0, R0, beta, gamma, T, dt=0.1):
    steps = int(T / dt) + 1
    t = np.linspace(0, T, steps)
    S, I, R = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    S[0], I[0], R[0] = S0, I0, R0
    for k in range(1, steps):
        dS = -beta * S[k-1] * I[k-1]
        dI = beta * S[k-1] * I[k-1] - gamma * I[k-1]
        dR = gamma * I[k-1]
        S[k] = S[k-1] + dt * dS
        I[k] = I[k-1] + dt * dI
        R[k] = R[k-1] + dt * dR
    return t, S, I, R

# ============================================================
# Helper: ODE SIS simulation (Euler)
# ============================================================
def sis_euler(I0, beta, gamma, T, dt=0.1):
    steps = int(T / dt) + 1
    t = np.linspace(0, T, steps)
    I = np.zeros(steps)
    I[0] = I0
    for k in range(1, steps):
        dI = beta * (1 - I[k-1]) * I[k-1] - gamma * I[k-1]
        I[k] = I[k-1] + dt * dI
    return t, I

# ============================================================
# Helper: ODE SEIR simulation (Euler)
# ============================================================
def seir_euler(S0, E0, I0, R0, beta, sigma, gamma, T, dt=0.1):
    steps = int(T / dt) + 1
    t = np.linspace(0, T, steps)
    S, E, I, R = [np.zeros(steps) for _ in range(4)]
    S[0], E[0], I[0], R[0] = S0, E0, I0, R0
    for k in range(1, steps):
        dS = -beta * S[k-1] * I[k-1]
        dE = beta * S[k-1] * I[k-1] - sigma * E[k-1]
        dI = sigma * E[k-1] - gamma * I[k-1]
        dR = gamma * I[k-1]
        S[k] = S[k-1] + dt * dS
        E[k] = E[k-1] + dt * dE
        I[k] = I[k-1] + dt * dI
        R[k] = R[k-1] + dt * dR
    return t, S, E, I, R

# ============================================================
# Helper: Well-mixed Agent-based SIR (no spatial structure)
# Each susceptible has a probability proportional to I/N of
# meeting an infected agent per time step, matching the ODE.
# ============================================================
def abm_sir_wellmixed(population=500, initially_infected=5, steps=200,
                     beta=0.35, gamma=0.10, seed=1):
    """Well-mixed stochastic SIR.  Each S agent independently meets
    one random agent per step; if that agent is I, infection occurs
    with probability beta.  Each I agent recovers with probability gamma."""
    rng = stdlib_random.Random(seed)
    # 1=S, 2=I, 3=R
    states = np.ones(population, dtype=int)
    states[:initially_infected] = 2

    s_hist, i_hist, r_hist = [], [], []
    for step in range(steps):
        nS = int(np.sum(states == 1))
        nI = int(np.sum(states == 2))
        nR = int(np.sum(states == 3))
        s_hist.append(nS)
        i_hist.append(nI)
        r_hist.append(nR)
        if nI == 0:
            # Epidemic is over; fill remaining steps
            for _ in range(steps - step - 1):
                s_hist.append(nS); i_hist.append(0); r_hist.append(nR)
            break
        new_states = states.copy()
        frac_I = nI / population
        for p in range(population):
            if states[p] == 1:
                # probability of contacting an infected agent
                if rng.random() < beta * frac_I:
                    new_states[p] = 2
            elif states[p] == 2:
                if rng.random() < gamma:
                    new_states[p] = 3
        states = new_states
    return np.array(s_hist), np.array(i_hist), np.array(r_hist)


# ============================================================
# 1. SIS STABILITY
# ============================================================
print('Generating SIS stability...')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

# R0 < 1
for I0 in [0.05, 0.15, 0.30, 0.50]:
    t, I = sis_euler(I0, beta=0.08, gamma=0.10, T=100)
    ax1.plot(t, I, lw=2, label=f'$I_0 = {I0}$')
ax1.set_title('$R_0 = 0.8 < 1$ (disease dies out)', fontweight='bold')
ax1.set_xlabel('Time')
ax1.set_ylabel('Infected fraction $I$')
ax1.set_ylim(-0.02, 0.55)
ax1.axhline(0, color='gray', lw=0.8, ls='--')
ax1.legend(fontsize=9)

# R0 > 1
for I0 in [0.01, 0.10, 0.30, 0.60, 0.90]:
    t, I = sis_euler(I0, beta=0.30, gamma=0.10, T=100)
    ax2.plot(t, I, lw=2, label=f'$I_0 = {I0}$')
endemic = 1 - 0.10 / 0.30
ax2.axhline(endemic, color='black', lw=1.5, ls='--', label=f'$I^* = {endemic:.2f}$')
ax2.set_title('$R_0 = 3.0 > 1$ (endemic equilibrium)', fontweight='bold')
ax2.set_xlabel('Time')
ax2.set_ylabel('Infected fraction $I$')
ax2.set_ylim(-0.02, 1.02)
ax2.legend(fontsize=9)

plt.tight_layout()
fig.savefig(f'{IMG}/sis_stability.pdf')
fig.savefig(f'{IMG}/sis_stability.png')
plt.close(fig)
print('  sis_stability done')

# ============================================================
# 2. SIR R0 COMPARISON
# ============================================================
print('Generating SIR R0 comparison...')
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
r0_values = [
    (0.15, 0.10, '$R_0 = 1.5$'),
    (0.25, 0.10, '$R_0 = 2.5$'),
    (0.50, 0.10, '$R_0 = 5.0$'),
]
for ax, (b, g, title) in zip(axes, r0_values):
    t, S, I, R = sir_euler(0.99, 0.01, 0.0, b, g, 160)
    ax.plot(t, S, color=C_S, lw=2, label='S')
    ax.plot(t, I, color=C_I, lw=2, label='I')
    ax.plot(t, R, color=C_R, lw=2, label='R')
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Fraction')
    ax.legend(fontsize=9)
    ax.set_ylim(-0.02, 1.02)
fig.suptitle('SIR Model: Effect of $R_0$', fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/sir_r0_comparison.pdf')
fig.savefig(f'{IMG}/sir_r0_comparison.png')
plt.close(fig)
print('  sir_r0_comparison done')

# ============================================================
# 3. SEIR DYNAMICS
# ============================================================
print('Generating SEIR dynamics...')
t, S, E, I, R = seir_euler(0.99, 0.0, 0.01, 0.0,
                            beta=0.5, sigma=0.2, gamma=0.1, T=200)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, S, color=C_S, lw=2, label='Susceptible')
ax.plot(t, E, color=C_E, lw=2, label='Exposed')
ax.plot(t, I, color=C_I, lw=2, label='Infected')
ax.plot(t, R, color=C_R, lw=2, label='Recovered')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Population fraction')
ax.set_title('SEIR Model Dynamics ($R_0 = 5$, latent period = 5 days)', fontweight='bold')
ax.legend()
ax.set_ylim(-0.02, 1.02)
plt.tight_layout()
fig.savefig(f'{IMG}/seir_dynamics.pdf')
fig.savefig(f'{IMG}/seir_dynamics.png')
plt.close(fig)
print('  seir_dynamics done')

# ============================================================
# 4. ODE vs ABM COMPARISON  (well-mixed ABM, same parameters)
# ============================================================
print('Generating ODE vs ABM comparison...')
pop = 500
beta_cmp = 0.35
gamma_cmp = 0.10
init_inf = 5
steps_cmp = 160

# ODE
t_ode, S_ode, I_ode, R_ode = sir_euler(
    S0=(pop - init_inf) / pop, I0=init_inf / pop, R0=0.0,
    beta=beta_cmp, gamma=gamma_cmp, T=steps_cmp, dt=0.1)

# Well-mixed ABM (single run)
s_abm, i_abm, r_abm = abm_sir_wellmixed(
    population=pop, initially_infected=init_inf, steps=steps_cmp,
    beta=beta_cmp, gamma=gamma_cmp, seed=7)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
t_abm = np.arange(len(i_abm))

# Left: ODE
ax1.plot(t_ode, S_ode * pop, color=C_S, lw=2, label='S')
ax1.plot(t_ode, I_ode * pop, color=C_I, lw=2, label='I')
ax1.plot(t_ode, R_ode * pop, color=C_R, lw=2, label='R')
ax1.set_title('ODE SIR (deterministic)', fontweight='bold')
ax1.set_xlabel('Time')
ax1.set_ylabel('Number of individuals')
ax1.legend()

# Right: ABM
ax2.plot(t_abm, s_abm, color=C_S, lw=2, label='S')
ax2.plot(t_abm, i_abm, color=C_I, lw=2, label='I')
ax2.plot(t_abm, r_abm, color=C_R, lw=2, label='R')
ax2.set_title('Well-mixed ABM (stochastic, one run)', fontweight='bold')
ax2.set_xlabel('Time step')
ax2.legend()

fig.suptitle(f'ODE vs Agent-Based SIR  ($R_0 = {beta_cmp/gamma_cmp:.1f}$, N = {pop})',
             fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/ode_vs_abm.pdf')
fig.savefig(f'{IMG}/ode_vs_abm.png')
plt.close(fig)
print('  ode_vs_abm done')

# ============================================================
# 5. ABM VARIABILITY  (well-mixed, many seeds, + ODE mean)
# ============================================================
print('Generating ABM variability...')
pop_var = 500
beta_var = 0.35
gamma_var = 0.10
steps_var = 160
init_var = 5

all_i = []
fig, ax = plt.subplots(figsize=(10, 5))
for seed in range(1, 21):
    _, i, _ = abm_sir_wellmixed(population=pop_var, initially_infected=init_var,
                                 steps=steps_var, beta=beta_var, gamma=gamma_var, seed=seed)
    all_i.append(i)
    ax.plot(i, color=C_I, lw=0.8, alpha=0.35)

# ODE reference (same parameters)
t_ref, _, I_ref, _ = sir_euler(
    (pop_var - init_var) / pop_var, init_var / pop_var, 0.0,
    beta_var, gamma_var, steps_var, dt=0.1)
ax.plot(t_ref, I_ref * pop_var, color='black', lw=3, label='ODE (deterministic)', zorder=5)

# Mean of ABM runs
mean_i = np.mean(all_i, axis=0)
ax.plot(mean_i, color=C_I, lw=2.5, ls='--', label='ABM mean (20 runs)', zorder=4)

ax.set_xlabel('Time step')
ax.set_ylabel('Infected agents')
ax.set_title(f'Stochastic Variability: 20 ABM runs vs ODE ($R_0 = {beta_var/gamma_var:.1f}$, N = {pop_var})',
             fontweight='bold')
ax.legend()
plt.tight_layout()
fig.savefig(f'{IMG}/abm_variability.pdf')
fig.savefig(f'{IMG}/abm_variability.png')
plt.close(fig)
print('  abm_variability done')

# ============================================================
# 6. POPULATION SIZE EFFECT  (well-mixed ABM)
# ============================================================
print('Generating population size effect...')
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
pop_sizes = [50, 500, 5000]
beta_pop = 0.35
gamma_pop = 0.10
steps_pop = 160

for ax, N in zip(axes, pop_sizes):
    n_inf0 = max(1, N // 100)
    # ODE reference
    t_ref, _, I_ref, _ = sir_euler((N - n_inf0)/N, n_inf0/N, 0.0,
                                    beta_pop, gamma_pop, steps_pop, dt=0.1)
    for seed in range(1, 11):
        _, i, _ = abm_sir_wellmixed(population=N, initially_infected=n_inf0,
                                     steps=steps_pop, beta=beta_pop, gamma=gamma_pop, seed=seed)
        ax.plot(i / N, color=C_I, lw=0.8, alpha=0.4)
    ax.plot(t_ref, I_ref, color='black', lw=2.5, label='ODE', zorder=5)
    ax.set_title(f'N = {N}', fontweight='bold')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Infected fraction')
    ax.set_ylim(-0.02, 0.55)
    ax.legend(fontsize=9)
fig.suptitle('Effect of Population Size on Stochastic Variability', fontweight='bold', fontsize=14)
plt.tight_layout()
fig.savefig(f'{IMG}/population_size_effect.pdf')
fig.savefig(f'{IMG}/population_size_effect.png')
plt.close(fig)
print('  population_size_effect done')

# ============================================================
# 7. VACCINATION EFFECT  (well-mixed ABM)
# ============================================================
print('Generating vaccination effect...')
def abm_sir_vacc(vacc_frac, population=500, initially_infected=5,
                 steps=160, beta=0.35, gamma=0.10, seed=1):
    """Well-mixed ABM with pre-vaccination."""
    rng = stdlib_random.Random(seed)
    states = np.ones(population, dtype=int)
    states[:initially_infected] = 2
    n_vacc = int(vacc_frac * (population - initially_infected))
    vacc_idx = list(range(initially_infected, population))
    rng.shuffle(vacc_idx)
    for idx in vacc_idx[:n_vacc]:
        states[idx] = 3

    i_hist = []
    for step in range(steps):
        nI = int(np.sum(states == 2))
        i_hist.append(nI)
        if nI == 0:
            for _ in range(steps - step - 1):
                i_hist.append(0)
            break
        new_states = states.copy()
        frac_I = nI / population
        for p in range(population):
            if states[p] == 1:
                if rng.random() < beta * frac_I:
                    new_states[p] = 2
            elif states[p] == 2:
                if rng.random() < gamma:
                    new_states[p] = 3
        states = new_states
    return np.array(i_hist)

fig, ax = plt.subplots(figsize=(10, 5))
vacc_fracs = [0.0, 0.2, 0.4, 0.6, 0.8]
colors_v = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(vacc_fracs)))
for vf, c in zip(vacc_fracs, colors_v):
    i = abm_sir_vacc(vf, population=500, steps=160, seed=42)
    ax.plot(i, color=c, lw=2, label=f'{int(vf*100)}% vaccinated')
ax.set_xlabel('Time step')
ax.set_ylabel('Infected agents')
ax.set_title('Effect of Vaccination on Epidemic Spread', fontweight='bold')
ax.legend()
plt.tight_layout()
fig.savefig(f'{IMG}/vaccination_effect.pdf')
fig.savefig(f'{IMG}/vaccination_effect.png')
plt.close(fig)
print('  vaccination_effect done')

# ============================================================
# 8. SEIR COVID EXAMPLE
# ============================================================
print('Generating SEIR COVID example...')
# COVID-like parameters: R0≈2.5, incubation≈5d, infectious≈10d
t, S, E, I, R = seir_euler(0.999, 0.0, 0.001, 0.0,
                            beta=0.25, sigma=0.2, gamma=0.1, T=250)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, S, color=C_S, lw=2, label='Susceptible')
ax.plot(t, E, color=C_E, lw=2, label='Exposed (incubating)')
ax.plot(t, I, color=C_I, lw=2, label='Infectious')
ax.plot(t, R, color=C_R, lw=2, label='Recovered')
ax.axvline(t[np.argmax(I)], color='gray', ls='--', lw=1, alpha=0.7)
ax.annotate(f'Peak: {np.max(I):.1%}', xy=(t[np.argmax(I)], np.max(I)),
            xytext=(t[np.argmax(I)]+20, np.max(I)+0.05),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=11, fontweight='bold')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Population fraction')
ax.set_title('SEIR Model — COVID-19-like Parameters ($R_0 \\approx 2.5$)', fontweight='bold')
ax.legend()
ax.set_ylim(-0.02, 1.02)
plt.tight_layout()
fig.savefig(f'{IMG}/seir_covid_example.pdf')
fig.savefig(f'{IMG}/seir_covid_example.png')
plt.close(fig)
print('  seir_covid_example done')

# ============================================================
# 9. SI ANALYTICAL SOLUTION
# ============================================================
print('Generating SI analytical solution...')
fig, ax = plt.subplots(figsize=(10, 5))
t_vals = np.linspace(0, 30, 500)
for beta_val in [0.2, 0.4, 0.8]:
    I0 = 0.01
    I_analytical = I0 / (I0 + (1 - I0) * np.exp(-beta_val * t_vals))
    ax.plot(t_vals, I_analytical, lw=2, label=f'$\\beta = {beta_val}$')
ax.axhline(0.5, color='gray', ls='--', lw=0.8, alpha=0.7)
ax.text(31, 0.50, '$I = 0.5$\n(inflection)', fontsize=9, va='center')
ax.set_xlabel('Time')
ax.set_ylabel('Infected fraction $I(t)$')
ax.set_title('SI Model: Analytical Solution (Logistic Growth)', fontweight='bold')
ax.legend()
ax.set_ylim(-0.02, 1.02)
plt.tight_layout()
fig.savefig(f'{IMG}/si_analytical.pdf')
fig.savefig(f'{IMG}/si_analytical.png')
plt.close(fig)
print('  si_analytical done')

# ============================================================
# 10. HERD IMMUNITY THRESHOLD
# ============================================================
print('Generating herd immunity threshold...')
R0_range = np.linspace(1.01, 20, 200)
p_herd = 1 - 1 / R0_range

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(R0_range, p_herd * 100, color='#8e44ad', lw=3)
ax.fill_between(R0_range, p_herd * 100, alpha=0.15, color='#8e44ad')
# Mark diseases
diseases = [('Influenza', 1.3), ('COVID-19', 2.5), ('Smallpox', 5.0),
            ('Mumps', 7.0), ('Measles', 15.0)]
for name, r0 in diseases:
    p = (1 - 1/r0) * 100
    ax.plot(r0, p, 'o', markersize=8, color='#e74c3c', zorder=5)
    ax.annotate(f'{name}\n$R_0={r0}$', xy=(r0, p),
                xytext=(r0 + 0.5, p - 8), fontsize=9)
ax.set_xlabel('Basic Reproduction Number $R_0$')
ax.set_ylabel('Herd Immunity Threshold (%)')
ax.set_title('Herd Immunity Threshold $p = 1 - 1/R_0$', fontweight='bold')
ax.set_xlim(1, 20)
ax.set_ylim(0, 100)
plt.tight_layout()
fig.savefig(f'{IMG}/herd_immunity.pdf')
fig.savefig(f'{IMG}/herd_immunity.png')
plt.close(fig)
print('  herd_immunity done')

print('\n=== All lesson 3 images generated ===')
