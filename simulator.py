
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider, Button

# ==========================================
# 2D GEOMETRIC TRANSFORMATION SIMULATOR
# ==========================================

# Original triangle
triangle = np.array([
    [1, 1],
    [4, 1],
    [2, 4]
], dtype=float)

# Homogeneous coordinates
points = np.column_stack(
    (triangle, np.ones(len(triangle)))
)

# Main window
fig = plt.figure(figsize=(14, 9))
fig.canvas.manager.set_window_title(
    "2D Geometric Transformation Simulator"
)

fig.suptitle(
    "2D GEOMETRIC TRANSFORMATION SIMULATOR",
    fontsize=17,
    fontweight="bold"
)

# Graph
ax = fig.add_axes([0.05, 0.22, 0.53, 0.68])

# Transformation choices
ax_radio = fig.add_axes([0.68, 0.53, 0.28, 0.40])

options = [
    "Translation",
    "Scaling",
    "Rotation",
    "Reflection X",
    "Reflection Y",
    "Reflection Origin",
    "Shear X",
    "Shear Y",
    "Composite"
]

radio = RadioButtons(ax_radio, options)

# Sliders
ax_s1 = fig.add_axes([0.15, 0.14, 0.42, 0.025])
ax_s2 = fig.add_axes([0.15, 0.08, 0.42, 0.025])

s1 = Slider(
    ax_s1, "Parameter 1",
    -5, 5, valinit=2, valstep=1
)

s2 = Slider(
    ax_s2, "Parameter 2",
    -5, 5, valinit=2, valstep=1
)

# Information panel
ax_info = fig.add_axes([0.66, 0.06, 0.32, 0.42])

# Reset button
ax_reset = fig.add_axes([0.82, 0.005, 0.15, 0.045])
reset_button = Button(ax_reset, "RESET")


# ==========================================
# TRANSFORMATION FUNCTION
# ==========================================

def update(event=None):

    choice = radio.value_selected
    a = s1.val
    b = s2.val

    # Translation
    if choice == "Translation":

        M = np.array([
            [1, 0, a],
            [0, 1, b],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = x + a\ny' = y + b"
        explanation = "Moves the triangle."

    # Scaling
    elif choice == "Scaling":

        M = np.array([
            [a, 0, 0],
            [0, b, 0],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = a * x\ny' = b * y"
        explanation = "Changes the size of the triangle."

    # Rotation
    elif choice == "Rotation":

        angle = np.deg2rad(a)

        M = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ], dtype=float)

        formula = (
            "x' = x cos(theta) - y sin(theta)\n"
            "y' = x sin(theta) + y cos(theta)"
        )

        explanation = f"Rotation by {a} degrees."

    # Reflection X
    elif choice == "Reflection X":

        M = np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = x\ny' = -y"
        explanation = "Reflection across X-axis."

    # Reflection Y
    elif choice == "Reflection Y":

        M = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = -x\ny' = y"
        explanation = "Reflection across Y-axis."

    # Reflection through origin
    elif choice == "Reflection Origin":

        M = np.array([
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = -x\ny' = -y"
        explanation = "Reflection through origin."

    # X Shearing
    elif choice == "Shear X":

        M = np.array([
            [1, a, 0],
            [0, 1, 0],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = x + a*y\ny' = y"
        explanation = "Horizontal shearing."

    # Y Shearing
    elif choice == "Shear Y":

        M = np.array([
            [1, 0, 0],
            [a, 1, 0],
            [0, 0, 1]
        ], dtype=float)

        formula = "x' = x\ny' = a*x + y"
        explanation = "Vertical shearing."

    # Composite: Scaling followed by translation
    elif choice == "Composite":

        S = np.array([
            [a, 0, 0],
            [0, a, 0],
            [0, 0, 1]
        ], dtype=float)

        T = np.array([
            [1, 0, b],
            [0, 1, b],
            [0, 0, 1]
        ], dtype=float)

        M = T @ S

        formula = (
            "Scaling followed by translation\n"
            "x' = a*x + b\n"
            "y' = a*y + b"
        )

        explanation = "Scaling first, then translation."

    # Apply transformation
    transformed = (M @ points.T).T
    new_triangle = transformed[:, :2]

    # Close triangle outlines
    original_closed = np.vstack(
        [triangle, triangle[0]]
    )

    new_closed = np.vstack(
        [new_triangle, new_triangle[0]]
    )

    # ==========================================
    # UPDATE GRAPH
    # ==========================================

    ax.clear()

    ax.plot(
        original_closed[:, 0],
        original_closed[:, 1],
        "bo-", linewidth=2, markersize=7,
        label="Original Triangle"
    )

    ax.plot(
        new_closed[:, 0],
        new_closed[:, 1],
        "ro-", linewidth=2, markersize=7,
        label="Transformed Triangle"
    )

    # Original vertex labels
    for i, label in enumerate(["A", "B", "C"]):
        ax.annotate(
            label,
            triangle[i],
            xytext=(5, 5),
            textcoords="offset points",
            color="blue"
        )

    # Transformed vertex labels
    for i, label in enumerate(["A'", "B'", "C'"]):
        ax.annotate(
            label,
            new_triangle[i],
            xytext=(5, 5),
            textcoords="offset points",
            color="red"
        )

    ax.axhline(0, color="black")
    ax.axvline(0, color="black")

    ax.grid(True)
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_aspect("equal", adjustable="box")

    ax.set_title("Original and Transformed Triangle")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend()

    # ==========================================
    # UPDATE INFORMATION PANEL
    # ==========================================

    ax_info.clear()
    ax_info.axis("off")

    matrix_text = np.array2string(
        M, precision=2, suppress_small=True
    )

    coordinates_text = np.array2string(
        new_triangle, precision=2, suppress_small=True
    )

    info = (
        f"TRANSFORMATION: {choice}\n\n"
        f"Explanation:\n{explanation}\n\n"
        f"MATHEMATICAL FORMULA:\n{formula}\n\n"
        f"TRANSFORMATION MATRIX:\n{matrix_text}\n\n"
        f"NEW COORDINATES:\n{coordinates_text}"
    )

    ax_info.text(
        0, 1, info,
        fontsize=8.5,
        verticalalignment="top",
        family="monospace"
    )

    fig.canvas.draw_idle()


# ==========================================
# RESET FUNCTION
# ==========================================

def reset(event):

    s1.reset()
    s2.reset()
    radio.set_active(0)


# ==========================================
# CONNECT ALL INTERACTIVE CONTROLS
# ==========================================

radio.on_clicked(update)
s1.on_changed(update)
s2.on_changed(update)

reset_button.on_clicked(reset)

# Initial display
update()

plt.show()
