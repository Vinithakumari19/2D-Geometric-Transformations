
import numpy as np
import matplotlib.pyplot as plt

# Original triangle
triangle = np.array([
    [1, 1],
    [4, 1],
    [2, 4]
])

# Homogeneous coordinates
points = np.column_stack((triangle, np.ones(len(triangle))))

# Scaling matrix
S = np.array([
    [2, 0, 0],
    [0, 2, 0],
    [0, 0, 1]
])

# Translation matrix
T = np.array([
    [1, 0, 3],
    [0, 1, 2],
    [0, 0, 1]
])

# Combine transformations
M = T @ S

# Apply combined transformation
transformed = (M @ points.T).T
new_triangle = transformed[:, :2]

# Display results
print("Original Coordinates:")
print(triangle)

print("\nCombined Transformation Matrix:")
print(M)

print("\nFinal Coordinates:")
print(new_triangle)

# Plot
plt.figure(figsize=(8, 8))

original_closed = np.vstack([triangle, triangle[0]])
transformed_closed = np.vstack([new_triangle, new_triangle[0]])

plt.plot(original_closed[:, 0], original_closed[:, 1],
         'bo-', label="Original Triangle")

plt.plot(transformed_closed[:, 0], transformed_closed[:, 1],
         'ro-', label="Scaled and Translated Triangle")

plt.axhline(0, color='black')
plt.axvline(0, color='black')

plt.grid(True)
plt.axis('equal')
plt.title("Composite Transformation: Scaling + Translation")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()

plt.show()
