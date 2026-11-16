# 2D Geometric Transformations in Computer Graphics Using Matrices

This project demonstrates 2D geometric transformations using homogeneous coordinates, 3 x 3 matrices, Python, NumPy and Matplotlib.

## Files

- `main.py` — batch calculations, numerical verification, comparison plots and image transformation using inverse mapping.
- `simulator.py` — interactive transformation simulator with selectable transformations and sliders.
- `matlab_demo.m` — corresponding MATLAB demonstration.
- `requirements.txt` — Python dependencies.

## Triangle used in the report

- A = (1, 1)
- B = (3, 1)
- C = (2, 3)

## Transformations included

Translation, scaling, rotation, reflection across the x-axis and y-axis, reflection through the origin, x-shear, y-shear, composite transformations, and rotation about the centroid.

## Installation

Install Python 3. Then open a terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
```

## Run the batch demonstration

```bash
python main.py
```

This prints numerical results and opens plots. It also demonstrates inverse-mapping image transformation.

## Run the interactive simulator

```bash
python simulator.py
```

Choose a transformation using the radio buttons. Adjust the sliders to change the parameters. Use Reset to return to the initial state.

## Mathematical representation

A point is represented in homogeneous coordinates as:

\[
P = [x, y, 1]^T
\]

The transformed point is:

\[
P' = MP
\]

where `M` is a 3 x 3 transformation matrix. For composite transformations, the rightmost matrix is applied first.

## Note

The MATLAB file is an additional demonstration and requires MATLAB. The Python programs can be run independently.
