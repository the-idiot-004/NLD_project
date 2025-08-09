from manim import *
import numpy as np
from PIL import Image
import colorsys

# === CONFIGURATION ===
MANDELBROT_WIDTH, MANDELBROT_HEIGHT = 1000, 1000
JULIA_WIDTH, JULIA_HEIGHT = 1000, 1000
MAX_ITER = 100
z = 0  # Global var for smooth coloring

# === COLORING ===
def get_color(n, max_iter):
    """Return smooth color based on iteration count."""
    if n == max_iter:
        return (0, 0, 0)  # black
    hue = (n + 1 - np.log(np.log(abs(z))) / np.log(2)) / max_iter
    hue = (hue * 2.5) % 1
    r, g, b = colorsys.hls_to_rgb(hue, 0.5, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))

# === FRACTAL CORE ===
def mandelbrot(c, max_iter):
    z_val = c
    for n in range(max_iter):
        if abs(z_val) > 2:
            return n, z_val
        z_val = z_val*z_val + c
    return max_iter, z_val

def julia(z_val, c, max_iter):
    for n in range(max_iter):
        if abs(z_val) > 2:
            return n, z_val
        z_val = z_val*z_val + c
    return max_iter, z_val

# === FRACTAL IMAGE GENERATION ===
def generate_mandelbrot_image(width, height, max_iter, x_range=(-2.0, 0.8), y_range=(-1.4, 1.4)):
    img = Image.new('RGB', (width, height), 'black')
    pixels = img.load()
    global z
    for x in range(width):
        for y in range(height):
            c = complex(
                x_range[0] + (x / width) * (x_range[1] - x_range[0]),
                y_range[0] + (y / height) * (y_range[1] - y_range[0])
            )
            n, z = mandelbrot(c, max_iter)
            pixels[x, y] = get_color(n, max_iter)
    return img

def generate_julia_image(c, width, height, max_iter, x_range=(-1.5, 1.5), y_range=(-1.5, 1.5)):
    img = Image.new('RGB', (width, height), 'black')
    pixels = img.load()
    global z
    for x in range(width):
        for y in range(height):
            z_init = complex(
                x_range[0] + (x / width) * (x_range[1] - x_range[0]),
                y_range[0] + (y / height) * (y_range[1] - y_range[0])
            )
            n, z = julia(z_init, c, max_iter)
            pixels[x, y] = get_color(n, max_iter)
    return img

# === MANIM SCENE ===
class MandelbrotJuliaMap(Scene):
    def construct(self):
        # Titles
        c_text = Text("c = 0.000 + 0.000i", font_size=36)
        title = Text("The Mandelbrot Set as a Map of Julia Sets", font_size=40)
        title_group = VGroup(c_text, title).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.3)
        self.play(Write(c_text), Write(title))
        self.wait(1)

        display_scale = 0.85

        # Mandelbrot display
        mandelbrot_img = generate_mandelbrot_image(MANDELBROT_WIDTH, MANDELBROT_HEIGHT, MAX_ITER)
        mandelbrot_mobject = ImageMobject(mandelbrot_img).scale(display_scale)
        mandelbrot_label = Text("Mandelbrot Set").scale(0.7).next_to(mandelbrot_mobject, DOWN, buff=0.2)
        mandelbrot_display = Group(mandelbrot_mobject, mandelbrot_label)

        # Julia placeholder
        julia_placeholder = Rectangle(width=mandelbrot_mobject.width, height=mandelbrot_mobject.height)
        julia_label = Text("Julia Set").scale(0.7).next_to(julia_placeholder, DOWN, buff=0.2)
        julia_display = Group(julia_placeholder, julia_label)

        # Group displays
        fractal_group = Group(mandelbrot_display, julia_display).arrange(RIGHT, buff=0.5)
        fractal_group.next_to(title_group, DOWN, buff=0.4)

        self.play(FadeIn(mandelbrot_mobject), Write(mandelbrot_label))
        self.play(Create(julia_placeholder), Write(julia_label))
        self.wait(1)

        # Animation path
        dot = Dot(color=YELLOW, radius=0.06)
        path = [
            complex(-0.745, 0.113),
            complex(-1.25, 0),
            complex(0.285, 0.01),
            complex(-0.8, 0.156),
            complex(0.4, 0.4),
            complex(-0.162, 1.04),
            complex(-0.70176, -0.3842),
            complex(0, 0),
        ]
        x_range_m = (-2.0, 0.8)
        y_range_m = (-1.4, 1.4)

        def get_dot_position(c_val):
            x_pos = np.interp(c_val.real, x_range_m, [mandelbrot_mobject.get_left()[0], mandelbrot_mobject.get_right()[0]])
            y_pos = np.interp(c_val.imag, y_range_m, [mandelbrot_mobject.get_bottom()[1], mandelbrot_mobject.get_top()[1]])
            return [x_pos, y_pos, 0]

        dot.move_to(get_dot_position(path[0]))
        self.play(Create(dot))

        def update_julia(c):
            julia_img = generate_julia_image(c, JULIA_WIDTH, JULIA_HEIGHT, MAX_ITER)
            return ImageMobject(julia_img).scale(display_scale).move_to(julia_placeholder)

        # Initial Julia
        julia_mobject_ref = update_julia(path[0])
        self.play(FadeIn(julia_mobject_ref), run_time=0.5)

        # Loop through points
        for c_val in path:
            new_dot_pos = get_dot_position(c_val)
            new_julia = update_julia(c_val)
            new_c_text = Text(f"c = {c_val.real:.3f} {c_val.imag:+.3f}i", font_size=36).move_to(c_text)

            self.play(
                dot.animate.move_to(new_dot_pos),
                Transform(julia_mobject_ref, new_julia),
                Transform(c_text, new_c_text),
                run_time=4
            )
            self.wait(2)

        self.wait(5)

