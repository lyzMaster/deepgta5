import math

import cv2
import numpy as np


prev_lines = [[], [], []]


def crop(image):

    return image[280:-130, :, :]


def grayscale(img):

    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold=100, high_threshold=300):

    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):

    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigmaX=30, sigmaY=30)


def region_of_interest(img, vertices):   #roi
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def construct_lane(lines):

    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []

    lane = [[], []]

    min_y = 0
    max_y = 190

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1) if x1 != x2 else 0  # <-- Calculating the slope.
                if 0.05 < math.fabs(slope) < 0.3:  # not interested
                    continue
                elif slope <= 0:  # <-- If the slope is negative, left group.
                    left_line_x.extend([x1, x2])
                    left_line_y.extend([y1, y2])
                else:  # <-- Otherwise, right group.
                    right_line_x.extend([x1, x2])
                    right_line_y.extend([y1, y2])

        offset = 7
        if left_line_x:
            poly_left = np.poly1d(np.polyfit(
                left_line_y,
                left_line_x,
                deg=1
            ))

            x1 = int(poly_left(max_y))
            x2 = int(poly_left(min_y))
            if prev_lines[0]:
                # recalculate x1
                if abs(x1 - prev_lines[0][0]) > offset:
                    x1 = prev_lines[0][0] - offset if prev_lines[0][0] > x1 else prev_lines[0][0] + offset
                # recalculate x2
                if abs(x2 - prev_lines[0][1]) > offset:
                    x2 = prev_lines[0][1] - offset if prev_lines[0][1] > x2 else prev_lines[0][1] + offset

            prev_lines[0] = [x1, x2]
            lane[0] = [x1, max_y, x2, min_y]
        elif prev_lines[0]:
            lane[0] = [prev_lines[0][0], max_y, prev_lines[0][1], min_y]
            prev_lines[0] = []

        if right_line_x:
            poly_right = np.poly1d(np.polyfit(
                right_line_y,
                right_line_x,
                deg=1
            ))

            x1 = int(poly_right(max_y))
            x2 = int(poly_right(min_y))
            if prev_lines[1]:
                # recalculate x1
                if abs(x1 - prev_lines[1][0]) > offset:
                    x1 = prev_lines[1][0] - offset if prev_lines[1][0] > x1 else prev_lines[1][0] + offset
                # recalculate x2
                if abs(x2 - prev_lines[1][1]) > offset:
                    x2 = prev_lines[1][1] - offset if prev_lines[1][1] > x2 else prev_lines[1][1] + offset

            prev_lines[1] = [x1, x2]
            lane[1] = [x1, max_y, x2, min_y]
        elif prev_lines[1]:
            lane[1] = [prev_lines[1][0], max_y, prev_lines[1][1], min_y]
            prev_lines[1] = []

    return lane


def hough_lines(img, rho=6, theta=np.pi / 120, threshold=160, min_line_len=60, max_line_gap=10):
    """
    `img` should be the output of a Canny transform.
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    return lines


def detect_lane(screen):
    # 0. Crop the image
    image = crop(screen)
    # 1. convert to gray
    image = grayscale(image)
    # 2. apply gaussian filter
    image = gaussian_blur(image, 7)
    # 3. canny
    image = canny(image, 50, 100)
    # 4. ROI
    image = region_of_interest(image, np.array([[(0, 190), (0, 70), (187, 0),
                                                 (613, 0), (800, 70), (800, 190)]], np.int32))
    # 5. Hough lines
    lines = hough_lines(image)
    # 6. construct lane
    return construct_lane(lines)
