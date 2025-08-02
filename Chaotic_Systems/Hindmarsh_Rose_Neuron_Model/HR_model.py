import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Hindmarsh-Rose model
def hr(state, t, r, I):
    x, y, z = state
    dx = y + 3*x**2 - x**3 - z + I
    dy = 1 - 5*x**2 - y
    dz = r * (4*(x + 1.6) - z)
    return np.array([dx, dy, dz])

# Basic RK4 integrator
def rk4(f, y0, t, r, I):
    dt = t[1] - t[0]
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        k1 = f(y[i-1], t[i-1], r, I)
        k2 = f(y[i-1] + 0.5*dt*k1, t[i-1] + 0.5*dt, r, I)
        k3 = f(y[i-1] + 0.5*dt*k2, t[i-1] + 0.5*dt, r, I)
        k4 = f(y[i-1] + dt*k3, t[i-1] + dt, r, I)
        y[i] = y[i-1] + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
    return y.T

# Parameters
r = 0.005
I_values = [1.2, 2.0, 3.2, 3.9]
initial_state = [-1.0, 0.0, 2.0]
t = np.linspace(0, 1200, 20000)

# Ploting
fig = plt.figure(figsize=(20, 6 * len(I_values)))
fig.suptitle("Hindmarsh-Rose Model Dynamics", fontsize=18)

for i, I in enumerate(I_values):
    x, y, z = rk4(hr, initial_state, t, r, I)
    start = 0 if np.std(x[len(x)//2:]) < 0.1 else len(x) // 2

    # (a) Phase space x–y
    ax1 = fig.add_subplot(len(I_values), 3, i*3 + 1)
    ax1.plot(x[start:], y[start:], lw=0.7)
    ax1.set_title(f'(a) Phase Space for I = {I:.2f}')
    ax1.set_xlabel('x'); ax1.set_ylabel('y'); ax1.grid(True)

    # (b) Time series x(t)
    ax2 = fig.add_subplot(len(I_values), 3, i*3 + 2)
    ax2.plot(t[start:], x[start:], lw=1)
    ax2.set_title(f'(b) Time Series for I = {I:.2f}')
    ax2.set_xlabel('t'); ax2.set_ylabel('x'); ax2.grid(True)
    if start == 0:
        m = np.mean(x[-100:])
        ax2.set_ylim(m - 0.05, m + 0.05)

    # (c) 3D trajectory
    ax3 = fig.add_subplot(len(I_values), 3, i*3 + 3, projection='3d')
    ax3.plot(x[start:], y[start:], z[start:], lw=0.5)
    ax3.set_title(f'(c) 3D Trajectory for I = {I:.2f}')
    ax3.set_xlabel('x'); ax3.set_ylabel('y'); ax3.set_zlabel('z')
    ax3.view_init(elev=20, azim=-60)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("hindmarsh_rose_dynamics.png", dpi=300)
plt.show()

