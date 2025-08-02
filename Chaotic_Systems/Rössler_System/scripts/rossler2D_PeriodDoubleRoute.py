import numpy as np
import matplotlib.pyplot as plt

# Rössler system equations
def rossler(state, t, a, b, c):
    x, y, z = state
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return np.array([dxdt, dydt, dzdt])

# RK4 integration method
def rk4(f, y0, t, a, b, c):
    dt = t[1] - t[0]
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        k1 = f(y[i-1], t[i-1], a, b, c)
        k2 = f(y[i-1] + 0.5*dt*k1, t[i-1] + 0.5*dt, a, b, c)
        k3 = f(y[i-1] + 0.5*dt*k2, t[i-1] + 0.5*dt, a, b, c)
        k4 = f(y[i-1] + dt*k3, t[i-1] + dt, a, b, c)
        y[i] = y[i-1] + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
    return y

# Integrate and remove transient
def compute_rossler(a, b, c, initial_state, T=300, dt=0.01, transient=220):
    t = np.arange(0, T, dt)
    sol = rk4(rossler, initial_state, t, a, b, c)
    cutoff = int(transient / dt)
    return sol[cutoff:, 0], sol[cutoff:, 1], sol[cutoff:, 2]

# Parameters and initial condition
a, b = 0.1, 0.1
initial_state = [0.1, 0.1, 0.1]
c_values = [5, 6, 8, 9, 12, 18]

# --- x–y projection ---
fig_xy = plt.figure(figsize=(14, 10))
plt.suptitle("Rössler Attractor: x–y Projection", fontsize=16)

for idx, c in enumerate(c_values):
    x, y, z = compute_rossler(a, b, c, initial_state)
    ax = fig_xy.add_subplot(3, 2, idx + 1)
    ax.plot(x, y, lw=0.5, color='red')
    ax.set_title(f"c = {c}", fontsize=11)
    ax.set_xlabel("x", fontsize=9)
    ax.set_ylabel("y", fontsize=9)
    ax.tick_params(labelsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig_xy.savefig("rossler_xy_projection.png", dpi=300, bbox_inches='tight')

# --- y–z projection ---
fig_yz = plt.figure(figsize=(14, 10))
plt.suptitle("Rössler Attractor: y–z Projection", fontsize=16)

for idx, c in enumerate(c_values):
    x, y, z = compute_rossler(a, b, c, initial_state)
    ax = fig_yz.add_subplot(3, 2, idx + 1)
    ax.plot(y, z, lw=0.5, color='darkgreen')
    ax.set_title(f"c = {c}", fontsize=11)
    ax.set_xlabel("y", fontsize=9)
    ax.set_ylabel("z", fontsize=9)
    ax.tick_params(labelsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig_yz.savefig("rossler_yz_projection.png", dpi=300, bbox_inches='tight')

# --- z–x projection ---
fig_zx = plt.figure(figsize=(14, 10))
plt.suptitle("Rössler Attractor: z–x Projection", fontsize=16)

for idx, c in enumerate(c_values):
    x, y, z = compute_rossler(a, b, c, initial_state)
    ax = fig_zx.add_subplot(3, 2, idx + 1)
    ax.plot(z, x, lw=0.5, color='navy')
    ax.set_title(f"c = {c}", fontsize=11)
    ax.set_xlabel("z", fontsize=9)
    ax.set_ylabel("x", fontsize=9)
    ax.tick_params(labelsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig_zx.savefig("rossler_zx_projection.png", dpi=300, bbox_inches='tight')

plt.show()

