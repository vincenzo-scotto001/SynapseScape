# utils.py
import random
import math
import ctypes
import numpy as np
import pyautogui


def generate_bezier_curve(start_pos, end_pos, complexity=8, steps=50):
    """Generate a smooth Bezier curve given start and end points using random midpoint displacement"""
    # Get the screen resolution
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Scale the points to match the screen resolution
    start_pos = (start_pos[0] * screen_width, start_pos[1] * screen_height)
    end_pos = (end_pos[0] * screen_width, end_pos[1] * screen_height)

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

        final_curve_points = []
        for t in np.linspace(0, 1, steps):
            x, y = _bezier(t, curve_points)
            final_curve_points.append((x, y))

    # Return the final curve points
    return final_curve_points


def smooth_move_bezier(start_pos, end_pos, duration=0.25, complexity=4, steps=50):
    """Move the mouse cursor smoothly along a Bezier curve generated using random midpoint displacement"""
    # Generate the Bezier curve
    curve_points = generate_bezier_curve(start_pos, end_pos, complexity, steps)

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

