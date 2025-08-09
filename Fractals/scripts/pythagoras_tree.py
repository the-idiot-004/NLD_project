import matplotlib.pyplot as plt
import numpy as np

def draw_branch(ax, x, y, length, angle, depth, max_depth):
    if depth > max_depth:
        return

    # Compute the end of the current branch
    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)

    # Line from (x, y) to (x_end, y_end) 
    ax.plot([x, x_end], [y, y_end], color='black', linewidth=1.2 * (1 - depth / max_depth))

    # Recursively draw the left and right branches
    new_length = length * 0.7
    draw_branch(ax, x_end, y_end, new_length, angle + np.pi / 6, depth + 1, max_depth)
    draw_branch(ax, x_end, y_end, new_length, angle - np.pi / 6, depth + 1, max_depth)

def main():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # Initial parameters
    start_x, start_y = 0, -1
    init_length = 1.0
    init_angle = np.pi / 2  # vertical

    max_depth = 15  # Increase for more complexity

    draw_branch(ax, start_x, start_y, init_length, init_angle, 0, max_depth)

    plt.tight_layout()
    plt.savefig("pythagoras_tree.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()
