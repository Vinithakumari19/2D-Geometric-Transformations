
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider, Button

# Triangle from the report
# A(1,1), B(3,1), C(2,3)

TRIANGLE = np.array([
    [1, 3, 2],
    [1, 1, 3],
    [1, 1, 1]
], dtype=float)


def translate(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


def scale(sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def rotate(degrees):
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ], dtype=float)


def shear_x(k):
    return np.array([
        [1, k, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype=float)


def shear_y(k):
    return np.array([
        [1, 0, 0],
        [k, 1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflect_x():
    return np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflect_y():
    return np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ], dtype=float)


def reflect_origin():
    return np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ], dtype=float)


def about_point(matrix, px, py):
    return translate(px, py) @ matrix @ translate(-px, -py)


def close_shape(points):
    return np.column_stack((points, points[:, 0]))


def format_matrix(matrix):
    return "\n".join(
        "[ " + "   ".join(f"{v:6.2f}" for v in row) + " ]"
        for row in matrix
    )


def main():

    options = [
        "Translation",
        "Scaling",
        "Rotation",
        "Reflection X",
        "Reflection Y",
        "Reflection Origin",
        "Shear X",
        "Shear Y",
        "Composite",
        "Rotate about centroid"
    ]

    # Large window for a spacious interface
    fig = plt.figure(figsize=(15, 10))

    try:
        fig.canvas.manager.set_window_title(
            "2D Geometric Transformations Simulator"
        )
    except Exception:
        pass

    fig.suptitle(
        "2D GEOMETRIC TRANSFORMATIONS USING MATRICES",
        fontsize=18,
        fontweight="bold",
        y=0.97
    )

    # --------------------------------
    # LEFT SIDE: GRAPH
    # --------------------------------

    ax = fig.add_axes([0.055, 0.12, 0.49, 0.78])

    ax.set_title("Transformation Visualization", fontsize=14, pad=12)
    ax.set_xlabel("X-axis", fontsize=11)
    ax.set_ylabel("Y-axis", fontsize=11)

    ax.axhline(0, color="black", linewidth=0.9)
    ax.axvline(0, color="black", linewidth=0.9)

    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-10, 12)
    ax.set_ylim(-10, 12)

    original = close_shape(TRIANGLE[:2])

    ax.plot(
        original[0], original[1],
        color="royalblue",
        marker="o",
        linewidth=2.5,
        markersize=7,
        label="Original"
    )

    transformed_line, = ax.plot(
        [], [],
        color="crimson",
        marker="o",
        linewidth=2.5,
        markersize=7,
        label="Transformed"
    )

    for label, (x, y) in zip("ABC", TRIANGLE[:2].T):
        ax.annotate("A (1, 1)", (1, 1),
            xytext=(-35, 12), textcoords="offset points",
            color="navy", fontsize=9)

        ax.annotate("B (3, 1)", (3, 1),
                    xytext=(8, -15), textcoords="offset points",
                    color="navy", fontsize=9)

        ax.annotate("C (2, 3)", (2, 3),
                    xytext=(8, 8), textcoords="offset points",
                    color="navy", fontsize=9)
        

    ax.legend(loc="upper left")

    # --------------------------------
    # RIGHT TOP: TRANSFORMATION MENU
    # --------------------------------

    
    radio_ax = fig.add_axes([0.62, 0.55, 0.34, 0.34])
    radio = RadioButtons(radio_ax, options, active=0)

    radio_ax.set_title(
        "CHOOSE TRANSFORMATION",
        fontsize=12,
        pad=12
    )

    # --------------------------------
    # RIGHT MIDDLE: SLIDERS
    # --------------------------------

    slider1_ax = fig.add_axes([0.70, 0.49, 0.23, 0.025])
    slider2_ax = fig.add_axes([0.70, 0.43, 0.23, 0.025])

    slider1 = Slider(
        slider1_ax,
        "Parameter 1",
        -5, 5,
        valinit=2,
        valstep=0.1
    )

    slider2 = Slider(
        slider2_ax,
        "Parameter 2",
        -5, 5,
        valinit=2,
        valstep=0.1
    )

    # --------------------------------
    # RESET BUTTON
    # --------------------------------
    reset_ax = fig.add_axes([0.78, 0.37, 0.14, 0.05])
    

    reset_button = Button(
        reset_ax,
        "RESET",
        color="whitesmoke",
        hovercolor="lightsteelblue"
    )

    # --------------------------------
    # INFORMATION PANEL
    # --------------------------------

    info_ax = fig.add_axes([0.61, 0.035, 0.36, 0.285])

    info_ax.set_facecolor("#f1f5f9")

    for spine in info_ax.spines.values():
        spine.set_edgecolor("#94a3b8")
        spine.set_linewidth(1.2)

    info_ax.set_xticks([])
    info_ax.set_yticks([])

    info_ax.set_title(
        "TRANSFORMATION DETAILS",
        fontsize=11,
        fontweight="bold",
        pad=9
    )

    info_text = info_ax.text(
        0.035,
        0.91,
        "",
        transform=info_ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        family="monospace",
        linespacing=1.2,
        color="#17212b"
    )

    # --------------------------------
    # UPDATE TRANSFORMATION
    # --------------------------------

    def update(_=None):

        choice = radio.value_selected

        p1 = slider1.val
        p2 = slider2.val

        if choice == "Translation":
            matrix = translate(p1, p2)
            explanation = "x' = x + tx;  y' = y + ty"

        elif choice == "Scaling":
            matrix = scale(p1, p2)
            explanation = "x' = sx*x;  y' = sy*y"

        elif choice == "Rotation":
            matrix = rotate(p1 * 18)
            explanation = f"Rotation: {p1 * 18:.1f} degrees"

        elif choice == "Reflection X":
            matrix = reflect_x()
            explanation = "Reflection across X-axis"

        elif choice == "Reflection Y":
            matrix = reflect_y()
            explanation = "Reflection across Y-axis"

        elif choice == "Reflection Origin":
            matrix = reflect_origin()
            explanation = "Reflection through origin"

        elif choice == "Shear X":
            matrix = shear_x(p1)
            explanation = "x' = x + k*y;  y' = y"

        elif choice == "Shear Y":
            matrix = shear_y(p1)
            explanation = "x' = x;  y' = y + k*x"

        elif choice == "Composite":
            matrix = translate(p1, p2) @ scale(2, 2)
            explanation = "Scaling by 2, then translation"

        else:
            angle = p1 * 18
            matrix = about_point(
                rotate(angle), 2, 5 / 3
            )
            explanation = f"Rotation about centroid: {angle:.1f} degrees"

        # Calculate transformed coordinates
        transformed = matrix @ TRIANGLE

        closed = close_shape(transformed[:2])

        transformed_line.set_data(
            closed[0],
            closed[1]
        )

        determinant = np.linalg.det(matrix[:2, :2])

        vertices = transformed[:2].T

        # Prepare neatly arranged information
        details = (
            f"Transformation: {choice}\n"
            f"{explanation}\n\n"
            f"Transformation Matrix:\n"
            f"{format_matrix(matrix)}\n\n"
            f"New Coordinates:\n"
            f"A ({vertices[0,0]:.2f}, {vertices[0,1]:.2f})\n"
            f"B ({vertices[1,0]:.2f}, {vertices[1,1]:.2f})\n"
            f"C ({vertices[2,0]:.2f}, {vertices[2,1]:.2f})\n"
            f"Determinant: {determinant:.3f}"
        )

        info_text.set_text(details)

        fig.canvas.draw_idle()

    # --------------------------------
    # RESET FUNCTION
    # --------------------------------

    def reset(_):

        slider1.reset()
        slider2.reset()
        radio.set_active(0)
        update()

    # Connect controls
    radio.on_clicked(update)
    slider1.on_changed(update)
    slider2.on_changed(update)
    reset_button.on_clicked(reset)

    update()

    plt.show()


if __name__ == "__main__":
    main()
