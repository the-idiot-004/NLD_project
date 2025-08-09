"""
Julia Set Fractal Renderer
Generates high-resolution images of famous Julia sets.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import re
from dataclasses import dataclass
from typing import Dict, Tuple


# ─── Configuration ─────────────────────────────────────────────────────────────
@dataclass
class JuliaConfig:
    width: int = 800
    height: int = 800
    x_min: float = -2.0
    x_max: float = 2.0
    y_min: float = -2.0
    y_max: float = 2.0
    max_iter: int = 1024
    escape_radius: float = 2.0
    log_scale_factor: float = 10.0


# ─── Julia Set Renderer ─────────────────────────────────────────────────────────
class JuliaSetRenderer:
    def __init__(self, config: JuliaConfig):
        self.config = config
        self.colormap = self._create_custom_colormap()

    def _create_custom_colormap(self) -> LinearSegmentedColormap:
        """Custom gradient color palette."""
        colors = [
            '#FF0000', '#FF4500', '#FF8C00', '#FFD700',
            '#FFFF00', '#ADFF2F', '#00FF00', '#008000'
        ]
        cmap = LinearSegmentedColormap.from_list("custom_palette", colors, N=256)
        cmap.set_bad(color='black')
        return cmap

    def compute_julia_set(self, c: complex) -> np.ndarray:
        """Compute escape values for the Julia set."""
        x = np.linspace(self.config.x_min, self.config.x_max, self.config.width)
        y = np.linspace(self.config.y_min, self.config.y_max, self.config.height)
        Z = x[None, :] + 1j * y[:, None]
        escape_values = np.zeros(Z.shape, dtype=float)
        mask = np.ones(Z.shape, dtype=bool)

        for i in range(self.config.max_iter):
            escaped = (np.abs(Z) > self.config.escape_radius) & mask
            if np.any(escaped):
                abs_z = np.abs(Z[escaped])
                nu = np.log(np.log(abs_z) / np.log(2)) / np.log(2)
                escape_values[escaped] = i + 1 - nu
                mask[escaped] = False
            if not np.any(mask):
                break
            Z[mask] = Z[mask] ** 2 + c
        return escape_values

    def process_escape_values(self, escape_values: np.ndarray) -> np.ma.MaskedArray:
        """Log-scale transform for smoother gradients."""
        scaled = np.where(
            escape_values > 0,
            np.log(escape_values + 1) * self.config.log_scale_factor,
            escape_values
        )
        return np.ma.masked_where(escape_values == 0, scaled)

    def get_color_range(self) -> Tuple[float, float]:
        """Fixed color scale for consistent visualization."""
        return 0, np.log(101) * self.config.log_scale_factor


# ─── Gallery  ───────────────────────────────────────────────
class JuliaSetGallery:
    FAMOUS_SETS: Dict[str, complex] = {
        "Classic Spiral": complex(-0.79, 0.15),
        "Douady's Rabbit": complex(-0.122561, 0.744862),
        "The San Marco Dragon": complex(0.285, 0.01),
        "Spiral Galaxy": complex(-0.75, 0.1),
        "The Basilica": complex(-1.0, 0.0),
        "Fatou Dust": complex(-0.4, 0.6),
        "Snowflake": complex(0.36, 0.1),
        "Cantor Dust": complex(0.5, 0.0)
    }

    def __init__(self, config: JuliaConfig):
        self.renderer = JuliaSetRenderer(config)
        self.config = config

    def create_single_figure(self, c: complex, name: str, figsize=(10, 10)) -> plt.Figure:
        """Render a single Julia set."""
        fig, ax = plt.subplots(figsize=figsize)
        escape_values = self.renderer.compute_julia_set(c)
        processed = self.renderer.process_escape_values(escape_values)
        vmin, vmax = self.renderer.get_color_range()
        ax.imshow(
            processed,
            extent=[self.config.x_min, self.config.x_max, self.config.y_min, self.config.y_max],
            cmap=self.renderer.colormap,
            origin='lower',
            vmin=vmin, vmax=vmax,
            interpolation='bilinear'
        )
        ax.axis('off')
        return fig

    def save_figure(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """Save image to file."""
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor='white')
        plt.close(fig)

    def generate_filename(self, name: str, c: complex) -> str:
        """Create safe filename from set name and c value."""
        safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
        c_str = f"{c.real:.6f}_{c.imag:.6f}i".replace('.', '_').replace('-', 'minus').replace('+', 'plus')
        return f"{safe_name}_c_{c_str}.png"

    def save_all_sets(self, dpi: int = 300):
        """Render and save all famous Julia sets."""
        for name, c in self.FAMOUS_SETS.items():
            fig = self.create_single_figure(c, name, figsize=(10, 10))
            filename = self.generate_filename(name, c)
            self.save_figure(fig, filename, dpi)


# ─── Main Execution ─────────────────────────────────────────────────────────────
def main():
    config = JuliaConfig(width=1200, height=1200, max_iter=1024)
    gallery = JuliaSetGallery(config)
    gallery.save_all_sets(dpi=300)


if __name__ == '__main__':
    main()

