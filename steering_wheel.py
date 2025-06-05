import numpy as np
import cv2
import math


def draw_steering_wheel(image, center_x, center_y, radius, angle_deg=0):
    """
    Draws a virtual steering wheel on a transparent image and rotates it by the given angle.

    Args:
        image (np.ndarray): The base image to draw the steering wheel on (should have 4 channels for transparency).
        center_x (int): X-coordinate of the wheel center.
        center_y (int): Y-coordinate of the wheel center.
        radius (int): Radius of the steering wheel.
        angle_deg (float): Angle in degrees to rotate the wheel (default is 0).

    Returns:
        np.ndarray: The image with the drawn and rotated steering wheel.
    """
    temp_wheel = np.zeros_like(image)
    cv2.circle(temp_wheel, (center_x, center_y), radius, (255, 255, 255, 255), 8)
    cv2.circle(temp_wheel, (center_x, center_y), radius // 4, (100, 100, 100, 255), -1)
    cv2.line(
        temp_wheel,
        (center_x - radius, center_y),
        (center_x - radius // 4, center_y),
        (200, 200, 200, 255),
        5,
    )
    cv2.line(
        temp_wheel,
        (center_x + radius, center_y),
        (center_x + radius // 4, center_y),
        (200, 200, 200, 255),
        5,
    )
    cv2.line(
        temp_wheel,
        (center_x, center_y - radius),
        (center_x, center_y - radius // 4),
        (200, 200, 200, 255),
        5,
    )
    rotation_matrix = cv2.getRotationMatrix2D((center_x, center_y), angle_deg, 1.0)
    rotated_wheel = cv2.warpAffine(
        temp_wheel, rotation_matrix, (image.shape[1], image.shape[0])
    )
    return rotated_wheel


def calculate_steering_angle(lx, ly, rx, ry):
    """
    Calculates the steering angle based on the positions of the left and right hands.

    Args:
        lx (int): X-coordinate of the left hand.
        ly (int): Y-coordinate of the left hand.
        rx (int): X-coordinate of the right hand.
        ry (int): Y-coordinate of the right hand.

    Returns:
        float: The calculated steering angle in degrees (negative for right, positive for left).
    """
    angle_rad = math.atan2(ry - ly, rx - lx)
    angle_deg = math.degrees(angle_rad)
    return -angle_deg
