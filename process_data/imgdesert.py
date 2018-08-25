import cv2
import numpy as np


def auto_canny(image_locate, sigma=0.33):
    image = cv2.imread(image_locate)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    v = np.median(blur_image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(blur_image, lower, upper)
    return edged


def roi(img, vertex):
    image = cv2.imread(img)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertex, [255, 255, 255])
    masked = cv2.bitwise_and(image, mask)
    return masked


