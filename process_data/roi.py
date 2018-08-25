import numpy as np
import cv2
import osdesert
import imgdesert

vertex = np.array([[0, 391], [0, 250], [750, 0], [850, 0], [1596, 300], [1596, 391]], np.int32)


def roi(img, vertex):
    image = cv2.imread(img)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertex, [255,255,255])
    masked = cv2.bitwise_and(image, mask)
    return masked


for file in osdesert.get_filename('/Users/lyz/Desktop/cannyed', 'jpg'):
    cv2.imwrite('/Users/lyz/Desktop/masked/'+file, roi('/Users/lyz/Desktop/cannyed/'+file, [vertex]))
