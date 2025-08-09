import matplotlib.pyplot as plt

def draw_cantor(x, y, length, depth, ax, max_depth):
    if depth == 0:
        return

    ax.hlines(y, x, x + length, color='black', linewidth=2)

    if x == 0.0:
        ax.text(-0.1, y, f"n = {max_depth - depth + 1}", fontsize=9,
                verticalalignment='center', horizontalalignment='right')

    new_length = length / 3
    new_y = y - 1.0 
    draw_cantor(x, new_y, new_length, depth - 1, ax, max_depth)
    draw_cantor(x + 2 * new_length, new_y, new_length, depth - 1, ax, max_depth)

def plot_cantor_set(depth=9):
    fig, ax = plt.subplots(figsize=(10, 6))
    draw_cantor(x=0.0, y=0.0, length=1.0, depth=depth, ax=ax, max_depth=depth)
    ax.set_xlim(-0.15, 1.05)  
    ax.set_ylim(-1.1 * (depth + 1), 1)
    ax.axis("off")
    ax.set_title(f"Cantor Set up to {depth} Iterations", fontsize=14)
    plt.tight_layout()
    plt.savefig("cantor_set.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_cantor_set(depth=9)

