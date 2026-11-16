"""
2D Geometric Transformations in Computer Graphics Using Matrices
Batch demonstration matching the accompanying experiential-learning report.

Run:
    python main.py

This script demonstrates:
- homogeneous-coordinate transformations
- composite transformations and order of operations
- rotation about the triangle centroid
- determinant/area checks
- orthogonality and inverse checks
- image transformation by inverse mapping
"""

import numpy as np
import matplotlib.pyplot as plt


# The report's test triangle: A(1,1), B(3,1), C(2,3).
# Each column is a homogeneous vertex; the first vertex is repeated to close it.
TRIANGLE = np.array(
    [[1, 3, 2, 1],
     [1, 1, 3, 1],
     [1, 1, 1, 1]],
    dtype=float
)


def translate(tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)


def scale(sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], dtype=float)


def rotate(degrees):
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def shear_x(k):
    return np.array([[1, k, 0], [0, 1, 0], [0, 0, 1]], dtype=float)


def shear_y(k):
    return np.array([[1, 0, 0], [k, 1, 0], [0, 0, 1]], dtype=float)


def reflect_x():
    return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)


def reflect_y():
    return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)


def reflect_origin():
    return np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)


def about_point(matrix, px, py):
    """Return a transformation matrix applied about (px, py)."""
    return translate(px, py) @ matrix @ translate(-px, -py)


def polygon_area(shape):
    """Shoelace area; shape is a 3 x n homogeneous matrix with closed polygon."""
    x, y = shape[0, :-1], shape[1, :-1]
    return 0.5 * abs(
        np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))
    )


def plot_cases(cases):
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    for ax, (name, matrix) in zip(axes.ravel(), cases.items()):
        transformed = matrix @ TRIANGLE
        ax.plot(TRIANGLE[0], TRIANGLE[1], "b-o", label="Original")
        ax.plot(transformed[0], transformed[1], "r-o", label="Transformed")
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.axvline(0, color="gray", linewidth=0.5)
        ax.set_title(name, fontsize=9)
        ax.set_aspect("equal")
        ax.grid(True)
        ax.legend(fontsize=8)
    for ax in axes.ravel()[len(cases):]:
        ax.set_visible(False)
    fig.suptitle("2D Geometric Transformations")
    plt.tight_layout()
    plt.show()


def warp_image(image, matrix, output_shape):
    """
    Transform an image using inverse mapping and nearest-neighbour sampling.
    matrix maps input coordinates to output coordinates.
    """
    height, width = output_shape
    ys, xs = np.mgrid[0:height, 0:width]
    output_coords = np.vstack(
        [xs.ravel(), ys.ravel(), np.ones(xs.size)]
    )
    source_coords = np.linalg.inv(matrix) @ output_coords

    sx = np.rint(source_coords[0]).astype(int)
    sy = np.rint(source_coords[1]).astype(int)
    valid = (
        (sx >= 0) & (sx < image.shape[1]) &
        (sy >= 0) & (sy < image.shape[0])
    )

    output = np.zeros(height * width, dtype=image.dtype)
    output[valid] = image[sy[valid], sx[valid]]
    return output.reshape(height, width)


def image_demo():
    # Synthetic 200 x 200 checkerboard with an asymmetric grey block.
    i, j = np.indices((200, 200))
    image = ((i // 20 + j // 20) % 2).astype(float)
    image[20:80, 20:60] = 0.5

    # Rotate 30 degrees and scale by 0.8 about the image centre.
    centre_x, centre_y = 100, 100
    matrix = about_point(
        rotate(30) @ scale(0.8, 0.8),
        centre_x, centre_y
    )
    result = warp_image(image, matrix, image.shape)

    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Original image")
    axes[1].imshow(result, cmap="gray")
    axes[1].set_title("Rotated 30° and scaled 0.8")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    centroid_x, centroid_y = 2, 5 / 3

    cases = {
        "Rotate 90 then scale 2": scale(2, 2) @ rotate(90),
        "Rotate then translate (4,0)": translate(4, 0) @ rotate(90),
        "Translate (4,0) then rotate": rotate(90) @ translate(4, 0),
        "Rotate 90 about centroid": about_point(
            rotate(90), centroid_x, centroid_y
        ),
        "Shear k=1": shear_x(1),
        "Reflect about x-axis": reflect_x(),
    }

    print("\\n2D GEOMETRIC TRANSFORMATIONS - NUMERICAL RESULTS\\n")
    for name, matrix in cases.items():
        transformed = matrix @ TRIANGLE
        print(name)
        print(np.round(transformed[:2, :-1], 3))
        determinant = np.linalg.det(matrix[:2, :2])
        print(
            "det =", round(determinant, 3),
            "| area =", round(polygon_area(transformed), 3),
            "\\n"
        )

    # Check orthogonality of a 45-degree rotation.
    rotation_45 = rotate(45)[:2, :2]
    print("R^T R = I ?", np.allclose(
        rotation_45.T @ rotation_45, np.eye(2)
    ))

    # Check inverse of a composite homogeneous transformation.
    composite = scale(2, 3) @ rotate(30) @ translate(1, 2)
    print("M^-1 M = I ?", np.allclose(
        np.linalg.inv(composite) @ composite, np.eye(3)
    ))

    # Display transformation comparison plots.
    plot_cases(cases)

    # Display image transformation using inverse mapping.
    image_demo()


if __name__ == "__main__":
    main()
