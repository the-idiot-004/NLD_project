"""
Fractal Renderer
================
Generates Mandelbrot and Julia set images with smooth coloring.

Output:
- output/mandelbrot.png
- output/julia_period_<n>.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ─── Configuration ────────────────────────────────────────────────────────────
OUTPUT_DIR = "output"           
WIDTH, HEIGHT = 1200, 1200       # Image resolution

# Complex plane boundaries
X_MIN, X_MAX = -2.0, 1.0
Y_MIN, Y_MAX = -1.5, 1.5

# Iteration settings
MAX_ITER = 1024
ESCAPE_RADIUS = 2.0
LOG_SCALE = 10.0

# c-values for Julia sets (periods 0–6)
C_VALUES = {
    0: 0 + 0j,
    1: -0.74543 + 0.11301j,
    2: -1.0 + 0j,
    3: -0.12256117 + 0.74486177j,
    4: -0.15652017 + 1.03224711j,
    5: -0.19804210 + 1.10026954j,
    6: -0.21752675 + 1.11445427j,
}

os.makedirs(OUTPUT_DIR, exist_ok=True)  


# ─── Colormap ──────────────────────────────────────────────────────────────────
def custom_colormap():
    """Custom gradient colormap for fractals."""
    colors = [
        '#FF0000', '#FF4500', '#FF8C00', '#FFD700',
        '#FFFF00', '#ADFF2F', '#00FF00', '#008000'
    ]
    cmap = LinearSegmentedColormap.from_list("custom_fractal", colors, N=256)
    cmap.set_bad(color='black')
    return cmap


C_MAP = custom_colormap()


# ─── Mandelbrot ────────────────────────────────────────────────────────────────
def compute_mandelbrot_escape(X, Y, max_iter=MAX_ITER):
    """Compute smooth escape-time values for Mandelbrot set."""
    Z = X + 1j * Y
    C = Z.copy()
    escape = np.zeros(Z.shape, float)
    mask = np.ones(Z.shape, bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] * Z[mask] + C[mask]       # z = z² + c
        escaped = mask & (np.abs(Z) > ESCAPE_RADIUS)
        if np.any(escaped):
            absZ = np.abs(Z[escaped])
            log_zn = np.log(absZ)
            nu = np.log(log_zn / np.log(2)) / np.log(2)
            escape[escaped] = i + 1 - nu            # smooth iteration count
            mask[escaped] = False
        if not mask.any():
            break

    return np.ma.masked_where(escape == 0, np.log(escape + 1) * LOG_SCALE)


def render_and_save_mandelbrot():
    """Render and save Mandelbrot image."""
    x = np.linspace(X_MIN, X_MAX, WIDTH)
    y = np.linspace(Y_MIN, Y_MAX, HEIGHT)
    X, Y = np.meshgrid(x, y)

    escape = compute_mandelbrot_escape(X, Y)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(
        escape, extent=[X_MIN, X_MAX, Y_MIN, Y_MAX],
        cmap=C_MAP, origin='lower', vmin=0, vmax=escape.max(),
        interpolation='bilinear'
    )
    ax.axis('off')
    fig.savefig(f"{OUTPUT_DIR}/mandelbrot.png", dpi=300,
                bbox_inches='tight', facecolor='black')
    plt.close(fig)
    print("[✔] Saved mandelbrot.png")


# ─── Julia ─────────────────────────────────────────────────────────────────────
def compute_julia_escape(c, max_iter=MAX_ITER):
    """Compute smooth escape-time values for Julia set with parameter c."""
    x = np.linspace(X_MIN, X_MAX, WIDTH)
    y = np.linspace(Y_MIN, Y_MAX, HEIGHT)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    escape = np.zeros(Z.shape, float)
    mask = np.ones(Z.shape, bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c                  # z = z² + c
        escaped = mask & (np.abs(Z) > ESCAPE_RADIUS)
        if np.any(escaped):
            absZ = np.abs(Z[escaped])
            log_zn = np.log(absZ)
            nu = np.log(log_zn / np.log(2)) / np.log(2)
            escape[escaped] = i + 1 - nu
            mask[escaped] = False
        if not mask.any():
            break

    return np.ma.masked_where(escape == 0, np.log(escape + 1) * LOG_SCALE)


def render_and_save_julia(period, c):
    """Render and save Julia set image for given c-value."""
    escape = compute_julia_escape(c)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(
        escape, extent=[X_MIN, X_MAX, Y_MIN, Y_MAX],
        cmap=C_MAP, origin='lower', vmin=0, vmax=escape.max(),
        interpolation='bilinear'
    )
    ax.axis('off')
    fig.savefig(f"{OUTPUT_DIR}/julia_period_{period}.png", dpi=300,
                bbox_inches='tight', facecolor='black')
    plt.close(fig)
    print(f"[✔] Saved julia_period_{period}.png")


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    """Generate Mandelbrot and Julia images."""
    render_and_save_mandelbrot()
    for period, c in C_VALUES.items():
        render_and_save_julia(period, c)


if __name__ == "__main__":
    main()

