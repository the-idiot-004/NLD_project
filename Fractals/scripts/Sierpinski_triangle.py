import matplotlib.pyplot as plt
import numpy as np

# Vertices of the triangle
vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])

# Initial point
point = np.array([0.25, 0.25])

#iter
iterations = 100000
points = []

# Chaos Game iteration
for _ in range(iterations):
    vertex = vertices[np.random.randint(0, 3)]
    point = (point + vertex) / 2
    points.append(point)

# Convert to array
points = np.array(points)

plt.figure(figsize=(8, 8))
plt.scatter(points[:, 0], points[:, 1], s=0.1, color='darkblue', alpha=0.5)
plt.axis('off')
plt.title("Sierpiński Triangle.", fontsize=16)
plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('Sierpiński Triangle.png',dpi=300)
plt.show()

