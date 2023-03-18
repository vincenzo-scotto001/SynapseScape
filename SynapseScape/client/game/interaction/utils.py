# utils.py
import random
import math
import ctypes
import numpy as np
import pyautogui


import random
import numpy as np
import pyautogui

def generate_bezier_curve(start_pos, end_pos, complexity=8, steps=50, window_size=(800, 600)):
    """Generate a smooth Bezier curve given start and end points using random midpoint displacement"""
    # Initialize the curve with the start and end points
    curve_points = [start_pos, end_pos]

    # Recursively apply midpoint displacement to generate the curve
    for i in range(complexity):
        new_points = []
        for j in range(len(curve_points) - 1):
            p1, p2 = curve_points[j], curve_points[j + 1]
            mid_x = int((p1[0] + p2[0]) / 2 + random.uniform(-10, 10))
            mid_y = int((p1[1] + p2[1]) / 2 + random.uniform(-10, 10))
            new_points.append(p1)
            new_points.append((mid_x, mid_y))
        new_points.append(end_pos)
        curve_points = new_points

    # Scale the curve points to match the game window size
    window_width, window_height = window_size
    scale_factor_x = window_width / 1.0
    scale_factor_y = window_height / 1.0
    curve_points_scaled = [(int(p[0] * scale_factor_x), int(p[1] * scale_factor_y)) for p in curve_points]

    # Generate the final Bezier curve with a higher number of steps
    final_curve_points = []
    for t in np.linspace(0, 1, steps):
        x, y = _bezier(t, curve_points_scaled)
        final_curve_points.append((x, y))

    # Return the final curve points
    return final_curve_points


def smooth_move_bezier(start_pos, end_pos, duration=0.25, complexity=4, steps=50, window_size=(800, 600)):
    """Move the mouse cursor smoothly along a Bezier curve generated using random midpoint displacement"""
    # Generate the Bezier curve
    curve_points = generate_bezier_curve(start_pos, end_pos, complexity, steps, window_size)

    # Calculate the duration between each step
    duration_per_step = duration / len(curve_points)

    # Move the mouse cursor along the Bezier curve
    for point in curve_points:
        pyautogui.moveTo(point[0], point[1], duration=duration_per_step)


def _bezier(t, control_points):
    """Calculate the position of a point on a Bezier curve given a parameter t and a list of control points"""
    n = len(control_points) - 1
    x = 0
    y = 0
    for i in range(n + 1):
        coeff = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
        coeff *= (1 - t)**(n - i) * t**i
        x += coeff * control_points[i][0]
        y += coeff * control_points[i][1]
    return x, y
