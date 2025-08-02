import numpy as np
import matplotlib.pyplot as plt

# Define Lorenz system
def lorenz_system(state, t, sigma, rho, beta):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return np.array([dxdt, dydt, dzdt])

# RK4
def rk4_step(f, state, t, dt, *params):
    k1 = dt * f(state, t, *params)
    k2 = dt * f(state + 0.5 * k1, t + 0.5 * dt, *params)
    k3 = dt * f(state + 0.5 * k2, t + 0.5 * dt, *params)
    k4 = dt * f(state + k3, t + dt, *params)
    return state + (k1 + 2*k2 + 2*k3 + k4) / 6.0

# Solve and discard transients
def solve_lorenz(rho, sigma=10.0, beta=8.0/3.0, 
                 x0=1.0, y0=1.0, z0=1.0, 
                 dt=0.005, n_steps=20000, n_transient=4000):
    state = np.array([x0, y0, z0])
    x_history = np.zeros(n_steps - n_transient)
    y_history = np.zeros(n_steps - n_transient)
    z_history = np.zeros(n_steps - n_transient)

    for i in range(n_steps):
        t = i * dt
        state = rk4_step(lorenz_system, state, t, dt, sigma, rho, beta)
        if i >= n_transient:
            idx = i - n_transient
            x_history[idx], y_history[idx], z_history[idx] = state

    return x_history, y_history, z_history

# Plot Lorenz attractors for different rho values
def plot_lorenz_bifurcations(rho_values, save_path='lorenz_period_doubling.png'):
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(16, 14))
    fig.suptitle('Lorenz System: Period-Doubling Route to Chaos', fontsize=22)

    for i, rho in enumerate(rho_values):
        ax = fig.add_subplot(2, 2, i + 1, projection='3d')
        print(f"Simulating for rho = {rho}...")
        x, y, z = solve_lorenz(rho=rho)

        ax.plot(x, y, z, color='blue', lw=0.5, alpha=0.8)
        ax.set_title(f"$\\rho = {rho}$", fontsize=16)
        ax.set_xlabel("X", fontsize=10)
        ax.set_ylabel("Y", fontsize=10)
        ax.set_zlabel("Z", fontsize=10)

        # Set plot styles
        ax.tick_params(colors='black')
        for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
            axis.pane.set_facecolor('white')
            axis.pane.set_edgecolor('lightgray')

        ax.grid(True, color='lightgray', linestyle='dotted', linewidth=0.5)
        ax.view_init(elev=25, azim=-120)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nPlot saved as '{save_path}'")
    plt.show()

# Run simulation for given rho values
if __name__ == '__main__':
    rho_list = [145, 148, 155, 166]
    plot_lorenz_bifurcations(rho_list)

