import matplotlib.pyplot as plt
import numpy as np


def lsystem_koch_snowflake(iterations):
    axiom = "F++F++F"
    rules = {"F": "F-F++F-F"}
    
    path = axiom
    for _ in range(iterations):
        path = "".join(rules.get(c, c) for c in path)

    return path

def draw_lsystem(path, angle=60, step=2):
    x, y = 0.0, 0.0
    theta = 0.0  # Start facing right
    coords = [(x, y)]

    for command in path:
        if command == "F":
            x += step * np.cos(np.radians(theta))
            y += step * np.sin(np.radians(theta))
            coords.append((x, y))
        elif command == "+":
            theta += angle
        elif command == "-":
            theta -= angle
    return np.array(coords)

def plot(coords, save_as="koch_snowflake.png"):
    plt.figure(figsize=(8, 8))
    plt.plot(coords[:, 0], coords[:, 1], color='darkblue', lw=0.5)
    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(save_as, dpi=300)
    plt.show()

if __name__ == "__main__":
    iterations = 6
    path = lsystem_koch_snowflake(iterations)
    coords = draw_lsystem(path, step=2)
    plot(coords)
