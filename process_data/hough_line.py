import numpy as np
import cv2
import osdesert

def hough(cannyed):
    image = cv2.imread(cannyed,0)  #不加0会报错！因为HoughLineP只能处理灰度图！
    minLineLength = 20
    maxLineGap = 15
    lines = cv2.HoughLinesP(image, 1, np.pi / 180, 180, minLineLength, maxLineGap)
    return lines

def draw_lines(img,lines):
    for line in lines:
        coords = line[0]
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)


for file in osdesert.get_filename('/Users/lyz/Desktop/masked', 'jpg'):
    lines = hough("/Users/lyz/Desktop/masked/" + file)
    img = cv2.imread("/Users/lyz/Desktop/masked/" + file)
    draw_lines(img,lines)
    cv2.imwrite("/Users/lyz/Desktop/masked/hough/"+file, img)
