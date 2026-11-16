
# 2D Geometric Transformations in Computer Graphics Using Matrices

## Project Overview

This project demonstrates 2D geometric transformations using mathematical matrices and Python programming.

It provides an interactive simulator that allows users to select transformations and observe how a triangle changes on a coordinate plane.

## Transformations Implemented

1. Translation
2. Scaling
3. Rotation
4. Reflection across X-axis
5. Reflection across Y-axis
6. Reflection through origin
7. X-axis Shearing
8. Y-axis Shearing
9. Composite Transformations

## Technologies Used

- Python
- NumPy
- Matplotlib

## Features

- Interactive transformation selection
- Adjustable parameter sliders
- Original and transformed triangle visualization
- Mathematical formula display
- Transformation matrix display
- Updated coordinate display
- Reset button

## Installation

Install Python, then install the required libraries:

```bash
pip install -r requirements.txt
```

## How to Run

Run the following command in the project folder:

```bash
python simulator.py
```

## Mathematical Concept

The project uses homogeneous coordinates and 3 x 3 matrices to perform geometric transformations.

A point is represented as:

\[
P = [x, y, 1]^T
\]

The transformed point is calculated using:

\[
P' = MP
\]

where M represents the transformation matrix.

## Project Objective

To understand the practical application of matrices in computer graphics through visualization and interactive experimentation.

## Developed For

Mathematics Experiential Learning Project
