import numpy as np
import matplotlib.pyplot as plt

# Rössler equations
def rossler(state, t, a, b, c):
    x, y, z = state
    dx = -y - z
    dy = x + a * y
    dz = b + z * (x - c)
    return np.array([dx, dy, dz])

# RK4 
def rk4(f, y0, t, a, b, c):
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        h = t[i] - t[i-1]
        k1 = f(y[i-1], t[i-1], a, b, c)
        k2 = f(y[i-1] + h/2 * k1, t[i-1] + h/2, a, b, c)
        k3 = f(y[i-1] + h/2 * k2, t[i-1] + h/2, a, b, c)
        k4 = f(y[i-1] + h * k3, t[i-1] + h, a, b, c)
        y[i] = y[i-1] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    return y

# Simulate and remove transient
def simulate_rossler(a, b, c, y0, T=300, dt=0.01, transient=220):
    t = np.arange(0, T, dt)
    sol = rk4(rossler, y0, t, a, b, c)
    cutoff = int(transient / dt)
    return sol[cutoff:, 0], sol[cutoff:, 1], sol[cutoff:, 2]

# Parameters
a, b = 0.1, 0.1
y0 = [0.1, 0.1, 0.1]
c_values = [5, 6, 8, 9, 12, 18]

# Plot results
fig = plt.figure(figsize=(14, 10))
plt.suptitle("Rössler Attractor: Varying c (a=0.1, b=0.1)", fontsize=16)

for i, c in enumerate(c_values):
    x, y, z = simulate_rossler(a, b, c, y0)
    ax = fig.add_subplot(3, 2, i + 1, projection='3d')
    ax.plot(x, y, z, lw=0.6, color='darkblue')
    ax.set_title(f"c = {c}", fontsize=11)
    ax.set_xlabel("x", fontsize=9)
    ax.set_ylabel("y", fontsize=9)
    ax.set_zlabel("z", fontsize=9)
    ax.tick_params(labelsize=8)
    ax.set_box_aspect([1, 1, 0.8])

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("rossler_3D.png", dpi=300, bbox_inches='tight')
plt.show()

