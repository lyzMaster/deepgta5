import numpy as np
import cv2


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

image = '/Users/lyz/Desktop/8BD28628513DC5E8EB356B23E5FC3516.jpg'
image = cv2.imread(image)
process_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
process_image = cv2.GaussianBlur(process_image, (3, 3), 0)
canny_image = cv2.Canny(process_image, 100, 200)
cv2.imwrite('/Users/lyz/Desktop/hand.jpg', canny_image)
auto_image = auto_canny(process_image)
cv2.imwrite('/Users/lyz/Desktop/auto.jpg', auto_image)
# cv2.imshow('image', process_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()